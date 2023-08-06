import os
import time
from contextlib import contextmanager

import cv2
import numpy as np
import pygame as pg
from pygame import surfarray


def pg_to_cv2(cvarray:np.ndarray)->np.ndarray:
    cvarray = cvarray.swapaxes(0,1) #rotate
    cvarray = cv2.cvtColor(cvarray, cv2.COLOR_RGB2BGR) #RGB to BGR
    return cvarray

def timer_wrapper(func):
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        #print("Finished:" ,func.__name__ ,end-start)
        return end - start
    return inner

@contextmanager
def timer(text):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(text, end-start)


@contextmanager
def video_writer(*args,**kwargs):
    video = cv2.VideoWriter(*args,**kwargs)
    try:
        yield video
    finally:
        video.release()

def surf_to_arr(frame: pg.Surface):
    try:
        pg_frame = surfarray.pixels3d(frame) # convert the surface to a np array. Only works with depth 24 or 32, not less
    except:
        pg_frame = surfarray.array3d(frame) # convert the surface to a np array. Works with any depth
    return pg_frame


@timer_wrapper
def save_video(frames: list, average_dt: float|list, file_type: str = "mp4", name: str = "screen_recording"):
    if type(average_dt) is list: average_dt = sum(average_dt)/len(average_dt) # force average_dt to be a float
    size = frames[0].get_size()
    codec_dict={
        "avi":'DIVX',
        "mp4":'MP4V'
    }
    codec = cv2.VideoWriter_fourcc(*codec_dict[file_type])
    with video_writer(name+"."+file_type, codec, 1000/average_dt, size) as video: # file_name, codec, average_fps, dimensions
        for frame in frames:
            pg_frame = surf_to_arr(frame)
            cv_frame = pg_to_cv2(pg_frame)  # then convert the np array so it is compatible with opencv
            video.write(cv_frame)   #write the frame to the video using opencv

@timer_wrapper
def save_frames(frames: list, dts: list, name: str = "screen_recording"):
    # instead of saving the images as a video, like any normal programmer, we save them as numpy images. 
    pg_arrays = (surf_to_arr(frame) for frame in frames)
    with timer("Finished saving"):
        np.savez_compressed(name+".npz",*pg_arrays,dts=np.array(dts),)

def draw_fps(s:pg.Surface,clock:pg.time.Clock): 
    fps = clock.get_fps()
    sysfont.render_to(s,(100,100),str(fps),fgcolor=nice_green)

# initializing globals (colors, fonts, window, etc.)
pg.init()
sysfont = pg.freetype.SysFont(None,40)
BLACK = (0,)*3
nice_green = pg.Color("chartreuse2")
size=(1000, 600)
pg.display.set_caption("Screen Recording")
window = pg.display.set_mode(size)
# this is to save the frames
frames = []
dts = []
clock = pg.time.Clock()

running=True
try:
    while running:
        dt = clock.tick(60) # aim for ... fps
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running=False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running=False
        window.fill(BLACK)
        draw_fps(window,clock)
        window_copy = window.copy() # if we don't copy the window then we will have the same image in all frames at the end
        frames.append(window_copy) # We save the current frame together with the time passed between the frames
        dts.append(dt)
        pg.display.flip()
        if len(frames) >= 100: running = False # uncomment this to stop the game after ... frames for similar results in every run"
finally:
    pg.quit()
    # At this stage, the game ended and the cleanup process can start. For this we convert the frames to opencv images
    # Only then we will write the video to the hard drive (That is what makes the save so slow).
    # General information about the recording
    frame_num = len(frames)
    dt_sum = sum(dts)
    average_dt = dt_sum/frame_num
    # This is only an approximation: 
    # for each frame we have width * height many pixels -> frame_num * width * height
    # A Surface needs get_bytesize() many bytes per pixel (In this case 4 bytes, because we set the depth of the display to 32 bits)
    memory_usage_approx = frame_num * size[0] * size[1] * frames[0].get_bytesize()  #https://www.pygame.org/docs/ref/surface.html#pygame.Surface.get_bytesize
    print("Total time:" , dt_sum/1000,"s")
    print("Average time per frame:" , average_dt,"ms")
    print("Memory usage approximation" , memory_usage_approx/1000, "KB")
    # args = (frames,dts,"avi","screen_recording")
    # time_for_save = save_video(*args)
    # file_name = args[3]+"."+args[2]
    args = (frames, dts, "screen_recording")
    time_for_save = save_frames(*args)
    file_name = args[2]+".npz"
    disk_memory_usage = os.path.getsize(file_name)
    print("Video memory usage:" , disk_memory_usage/1000, "KB")
    with open("test.txt", "a") as f:
        print("Total video length:" , dt_sum/1000,"s\nNumber of frames:", frame_num,"\nFPS:",1000/average_dt,"\nSize:",size,"\nTime for save:",time_for_save,"s\nSaved in file:",file_name,"with",disk_memory_usage/1000, "KB memory",file=f)
        print("_"*100,file=f)
