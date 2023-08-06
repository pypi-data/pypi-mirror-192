"""
This module should use pipes to ffmpeg and async functions to easily record the screen
"""

import asyncio
import os
import subprocess as sp
import time
from abc import ABC, abstractmethod
from asyncio import Event
from contextlib import redirect_stdout

import cv2
import numpy as np
import pygame as pg
from pygame import freetype
from pygame.surface import Surface

# time helper functions; 

def _get_time(): return time.perf_counter()
_time_since = lambda t: _get_time()-t
_sleep = lambda t: time.sleep(t)

class _ScreenPiper(ABC):
    @abstractmethod
    def __init__(self, fps: float, filename: str, s: Surface = None):
        raise NotImplementedError()

    @abstractmethod
    def start(self):
        raise NotImplementedError()
    
    @abstractmethod
    def stop(self): 
        raise NotImplementedError()

class FFMPEGPiper(_ScreenPiper):
    # Vastly copied from pygame-screen-recorder
    def __init__(self, fps: float, filename: str, s: Surface = None):
        self.fps = fps
        self.filename = filename
        self.s = s or pg.display.get_surface()

        self.dtf = 1/fps # in secs
        self.pipe = None
        self.stopped = False
        self.finished_event = Event()
    
    async def start(self):
        width, height = self.s.get_size()
        size = f"{width}x{height}"
        with open(os.devnull, 'w') as nul, redirect_stdout(nul):
            self.pipe = asyncio.Popen(['ffmpeg',
                '-v','fatal',
                '-y', 
                '-f', 'rawvideo',
                '-vcodec','rawvideo',
                '-s', size,
                '-pix_fmt','rgba',
                '-r',str(self.fps),
                '-i','-',
                '-an',
                '-vcodec', 'qrtl',
                    self.filename], stdin=sp.PIPE, stdout=nul)
        asyncio.ensure_future(self.loop())

    def stop(self):
        if self.pipe is not None:
            asyncio.get_event_loop().run_until_complete(self._stop())
        else:
            raise ValueError("The Piper was stopped without being started")

    async def _stop(self):
        self.stopped = True
        await self.finished_event.wait()
        
        self.pipe.stdin.close()
        self.pipe.wait()

    async def loop(self):
        while True:
            print("looping")
            if self.stopped: 
                return self.finished_event.set()
            before = _get_time() # ns
            await self.push_frame()
            wait = max(0,self.dtf-(_time_since(before)))
            time.sleep(wait)


    async def push_frame(self):
        r = pg.surfarray.pixels_red(self.s)
        g = pg.surfarray.pixels_green(self.s)
        b = pg.surfarray.pixels_blue(self.s)
        a = np.ones_like(r)*255

        #merge the rgba channels
        mergedImage = cv2.merge((r,g,b,a))

        #rotate the image 90 degrees
        rows,cols,draws = mergedImage.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),-90,1)
        rotatedMergedImage = cv2.warpAffine(mergedImage,M,(cols,rows))

        #flip the image horizontally
        rotatedMergedImage = cv2.flip(rotatedMergedImage,1)

        #create a mask of black pixels
        black = rotatedMergedImage[:,:,0] == 0

        #apply the mask to the frame buffer
        rotatedMergedImage[black] = [0,0,0,0]

        #feed the frame buffer to the ffmpeg pipe
        self.pipe.stdin.write(rotatedMergedImage)
        
        r = []
        g = []
        b = []
        a = []
        

async def main():
    pg.init()
    WINDOW_WIDTH, WINDOW_HEIGHT = screenSize = pg.Vector2(400,400)
    screen = pg.display.set_mode(screenSize)

    clock = pg.time.Clock()
    font = freetype.SysFont("MonoLisa", size = 30)
    counter = 0

    piper = FFMPEGPiper(60,"newvideo.mov")
    await piper.start()

    try:
        while True:
            clock.tick(10)
            if any(event.type == pg.QUIT for event in pg.event.get()):
                return
            screen.fill("black")
            font.render_to(screen,(175,175),str(counter),"green")
            counter+=1
            pg.display.flip()
            if counter>500:
                return

    finally:
        pg.quit()
        await piper._stop()

if __name__ == '__main__':
    # demo
    asyncio.run(main())
