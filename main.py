import cv2
import os
import time

import video
import utils

frame_count = 0
for frame in video.extract_video("./bad_apple.webm"):
  os.system("clear")
  
  img = video.process_frame(frame, height=7)
  height, width, channels = img.shape
  
  print(video.render_frame(img))
  print(f"Frame: {frame_count}")
  
  
  for y in range(height):
    for x in range(width):
      pixel = img[y,x][0]
      
  
  time.sleep(1/30)
  frame_count += 1
