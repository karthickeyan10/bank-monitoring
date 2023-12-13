from easygui import *
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string
while 1:
  image   = "signlang.png"
  msg="                             VIDEO MONITORING SYSTEM FOR BANKS"
  choices = ["Tampering Detection","Count the people","Sentiment Analysis"]
  reply   = buttonbox(msg,image=image,choices=choices)
  if reply ==choices[0]:
        from camera_tampering_detection import cap
  if reply == choices[2]: 
        from live_cam_predict import cap
  if reply==choices[1]:
       from counter import cap 
       