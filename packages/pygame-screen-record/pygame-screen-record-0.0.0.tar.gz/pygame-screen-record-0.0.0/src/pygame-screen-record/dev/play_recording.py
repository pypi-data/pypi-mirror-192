import time
from contextlib import contextmanager

import cv2
import numpy as np
import pygame as pg
from pygame import surfarray

pg.init()
WHITE = (255,)*3
size = (1920, 816)

@contextmanager
def timer(text):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(text, end-start)

cv2_to_pg = lambda arr: cv2.cvtColor(arr.swapaxes(0,1), cv2.COLOR_BGR2RGB)

def play_video_file(filename: str = "saved_files/Narnia_01_Original.mp4"):
    video = cv2.VideoCapture(filename)
    if (video.isOpened()):
        pg.display.set_caption("Showing Video")
        SCREEN = pg.display.set_mode(size,depth=32)
        running = True
        clock = pg.time.Clock()
        with timer("Finished playing"):
            while running:
                clock.tick(60)
                for event in pg.event.get():
                    if event.type == pg.QUIT: 
                        running=False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            running=False
                running,cv_frame = video.read()
                if not running: break
                pg_frame=cv2_to_pg(cv_frame)
                surfarray.blit_array(SCREEN,pg_frame)
                pg.display.flip()
    video.release()


def gen_frames(npz: np.lib.npyio.NpzFile):
    """Supplies the numpy frames and delays the yield to maintain the correct delta time between frames. """
    def get_time(): # in ms
        return time.time()*1000
    def time_since(t): # in ms
        return get_time()-t
    files=npz.files
    dts = npz["dts"]
    assert files.pop(0) == "dts", "First array must be dts"
    last = get_time()
    for k,dt in zip(files,dts):
        pg_array = npz[k]
        diff = dt - time_since(last)
        print(k,dt,diff)
        if diff > 0:
            pg.time.delay(int(diff))
        last = get_time()
        yield pg_array

def play_frames(filename: str = "screen_recording.npz"):
    npzFile: np.lib.npyio.NpzFile = np.load(filename)
    #print(np.info(npzFile))
    pg.display.set_caption("Showing Video")
    SCREEN = pg.display.set_mode(size,depth=32)
    with timer("Finished playing"):
        for frame in gen_frames(npzFile):
            if frame is None:break
            surfarray.blit_array(SCREEN,frame)
            for event in pg.event.get():
                if event.type == pg.QUIT: break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE: break
            pg.display.flip()

play_video_file()
#play_frames()

pg.quit()
#np.savez()
