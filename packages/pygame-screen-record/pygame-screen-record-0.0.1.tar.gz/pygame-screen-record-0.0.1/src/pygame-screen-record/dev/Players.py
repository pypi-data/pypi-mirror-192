import atexit, itertools, logging, os, time, threading
import math
from contextlib import contextmanager
from functools import cache, wraps
from threading import Thread
from types import GenericAlias
from typing import (Callable, Coroutine, List, Literal, Optional,
                    SupportsIndex, Tuple, Type, _GenericAlias,
                    _UnionGenericAlias)

import cv2
import numpy as np
import pygame as pg

from ScreenRecorder import AnyPath, Anypath_type, available_formats, PlayingThread, Preloader


class Preloader(PlayingThread): 
    def __init__(self, get_frames: Callable[[int],pg.Surface],thread: PlayingThread, max_preload:int = 100):
        self.get_frames = get_frames
        self.thread = thread
        self.max_preload = max_preload
    def run(self): 
        while self.running:
            if self.position-self.thread.position<self.max_preload:
                try:
                    self.get_frames(self.position)
                    self.position+=1
                except (IndexError):
                        break



_props = {
    "width":cv2.CAP_PROP_FRAME_WIDTH,
    "height":cv2.CAP_PROP_FRAME_HEIGHT,
    "fps":cv2.CAP_PROP_FPS,
    "frame_count":cv2.CAP_PROP_FRAME_COUNT
}

video_properties = list(_props.keys())+["size","all"]
""" The list of properties a video may have """

class Video:
    """ Represents a Video Source. """
    def __init__(self,source: AnyPath | int):
        """ Inits a Video
        
        Parameters
        ----------
        source: AnyPath | int | cv2.VideoCapture 
            If path, opens that file as a stream 
            if int, then opens the i-th camera as stream.
        """
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            try:
                with open(source) as _: 
                    if type(source) is str: 
                        assert source.split(".")[-1] in available_formats # Test if file can be opened
            except:
                problem = "File cannot be opened currently" if os.path.isfile(source) else "File/Camera doesn't exist/cannot be opened"
                raise ValueError(problem+": "+str(source))
        assert isinstance(source,Anypath_type),("source has to be a path or an int")

    def __del__(self):
        self.cap.release()

    def play(self,*args,**kwargs)->'VideoPlayer':
        """ 
        Creates a VideoPlayer object, starts playing it, and returns it. 
        All args and kwargs will be passed to VideoPlayer
        """
        vip = VideoPlayer(self,*args,*kwargs)
        vip.play()
        return vip
    
    @cache
    def __getattr__(self, prop: Literal["width","height","fps","frame_count","size","all"] | int | str) -> int|float:
        """ Returns the given property of the video """
        if type(prop) is int:
            return self.cap.get(prop)
        elif type(prop) is str:
            cv_prop = _props.get(prop)
            if cv_prop is not None:
                result = self.cap.get(cv_prop)
                if prop == "fps":
                    return result
                else:
                    return int(result)
            elif prop == "size":
                return self.width,self.height
            elif prop == "all":
                return tuple(self.__getattr__(prop) for prop in video_properties)
            return self.__getattribute__(prop)

class VideoPlayer:
    """ 
    This is a very naive VideoPlayer. Please do not use it for large Videos (like Movies). 
    It is rather intended for small animations or little Recordings that might be replayed a lot of times
    """
    def __init__(self,source: AnyPath | Video, surf: Optional[pg.Surface] = None, on_stop: Optional[Callable[[],None]] = None, always_load: bool = True):
        """always_load(bool): Whether to always load the full video until the given position when seeking"""
        if isinstance(source,Video):
            self.video = source
        else:
            self.video = Video(source)
        self.surf = surf or pg.display.get_surface()
        self.on_stop = on_stop or mt
        self.always_load = always_load
        if not self.cap.isOpened(): raise RuntimeError("Video isn't opened")
        self.will_scale = not self.size == self.surf.get_size()
        if self.will_scale: 
            logging.warning("Video size doesn't match surface size. Will be rescaled")
            self.scale = self.surf.get_size()
        self.frames = [None]*self.frame_count
        self.max_preload = int(0.2 * math.log(len(self.frames)))
        logging.debug("Max Preload of video: "+str(self.max_preload))
        self._init_thread()
    
    def _on_stop(self):
        ret_val = self.on_stop()
        if ret_val is False: 
            self._init_thread()
        elif ret_val is True:
            self.play()

    def _init_thread(self): 
        """ Internal function to init a new thread """
        new_thread = PlayingThread(self.surf,1000/self.fps,self._get_frames,self._on_stop)
        logging.debug(f"Initing new Thread ({new_thread.name}) of {self.__class__.__name__}")
        try:
            new_thread.position = self.thread.position
        except NameError:
            pass
        self.thread= new_thread
    def _init_thread(self):        
        self.thread = PlayingThread(self.surf, 1000/self.fps, self._get_frames,self._on_stop)
        self.loader = Preloader(self._get_frames,self.thread,self.max_preload)
        
    def __getattr__(self, key):
        try:
            return self.video.__getattr__(key)
        except NameError: 
            return self.__getattribute__(key)

    @property
    def position(self): 
        return int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

    @position.setter
    def _(self)->None:
        self.cap.set(cv2.CAP_PROP_POS_FRAMES)

    def _get_frames(self, position: int):
        """ Internal function to get the frame at a specific position """
        frame = self.frames[position]
        while frame is None:
            self._get_next()
            frame = self.frames[position]
        return frame
    
    def _get_next(self)->pg.Surface:
        """ Internal function to get the next frame """
        position = self.position
        logging.debug("Getting next frame at position: "+str(position))
        ret,cv_frame = self.cap.read()
        if not ret: raise IndexError
        surf = pg.surfarray.make_surface(_cv2_to_pg(cv_frame))
        if self.will_scale:
            surf = pg.transform.scale(surf,self.scale)
        self.frames[position] = surf
        return surf

    def stop(self):
        super().stop() # stops the thread
        self.loader.stop()
        self.cap.release()

    def seek(self,position:int)->None:
        if self.always_load: self.position = position
        self.loader.position = position
        return super().seek(position)

    def reuse(self,new_on_stop: Optional[Callable[[],None]] = None)->'RecordingPlayer':
        if not self.is_("loaded"): 
            if self.is_("stopped"):
                raise RuntimeError("Reusing a not fully loaded stopped VideoPlayer.")
            else: 
                logging.warning("Reusing a not fully loaded Player. Might take a while")
                unloadPlayer(self)
                assert self.is_("loaded")
        rec = Recording(self["fps"],self["size"])
        rec.frames = self.frames
        on_stop = new_on_stop or self.on_stop
        return RecordingPlayer(rec,on_stop,self.surf)
    

