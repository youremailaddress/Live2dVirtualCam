'''
 @Date: 2022-05-18 10:16:26
 @LastEditors: Wu Han
 @LastEditTime: 2022-05-18 20:08:56
 @FilePath: \test\test.py
'''
import pyvirtualcam
import numpy as np
import time

with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
    while True:
        frame = np.zeros((cam.height, cam.width, 4), np.uint8) # RGBA
        frame[:,:,:3] = cam.frames_sent % 255 # grayscale animation
        frame[:,:,3] = 255
        cam.send(frame)
        cam.sleep_until_next_frame()
        # break
        # time.sleep(1/60)