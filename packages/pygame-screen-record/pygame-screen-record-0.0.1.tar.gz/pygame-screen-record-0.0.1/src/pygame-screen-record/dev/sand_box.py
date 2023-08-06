import pygame as pg
from pygame import surfarray
import numpy as np
import cv2

pg.init()

WHITE = 255, 255, 255

def show_image(image:pg.Surface|np.ndarray):
    pg.display.set_caption("Showing Image")

    if type(image)==pg.Surface:
        rect = image.get_rect()
        size = rect.size
        SCREEN = pg.display.set_mode(size,depth=32)
        SCREEN.blit(image,rect)
    elif type(image)==np.ndarray:
        size = image.shape[0:2]
        SCREEN = pg.display.set_mode(size,depth=32)
        surfarray.blit_array(SCREEN,image)

    pg.display.flip()

    running=True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                running=False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running=False

def create_nice_shape():
    #from: https://stackoverflow.com/questions/41168396/how-to-create-a-pygame-surface-from-a-numpy-array-of-float32
    x = np.arange(0, 300)
    y = np.arange(0, 300)
    X, Y = np.meshgrid(x, y)

    Z = X + Y
    #Z looks like this (if it wasn't (300,300) but (4,4)): 
    """
    [0,1,2,3]
    [1,2,3,4]
    [2,3,4,5]
    [3,4,5,6]
    """

    Z:np.ndarray = 255*Z/Z.max() #normalize Z to 255
    return Z

#from: https://gist.github.com/radames/1e7c794842755683162b
cv2_to_pg = lambda arr: cv2.cvtColor(arr.swapaxes(0,1), cv2.COLOR_BGR2RGB)

pg_to_cv2 = lambda arr: cv2.cvtColor(arr.swapaxes(0,1), cv2.COLOR_RGB2BGR)

# from numpy to pygame surface
# array = create_nice_shape()
# show_array_double(array)

# pure_cvarray=cv2.imread('crow_test.jpg',cv2.IMREAD_UNCHANGED)

# pgarray = surfarray.array3d(pg.image.load('crow_test.jpg'))

# cv2.imshow("win",pg_to_cv2(pgarray))

# array = cv2_to_pg(pure_cvarray)

# show_image(array)

# cv2.destroyAllWindows()
