#module for video processing

import cv2
import math

def extract_video(path):
  capture = cv2.VideoCapture(path)
  success = True

  while success:
    success, img = capture.read()
    
    if success:
      yield img
    
def process_frame(img, height):
  img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
  
  ratio = height / img.shape[0]
  newsize = math.ceil(img.shape[1]*ratio), height
  
  img = cv2.resize(img, newsize, interpolation=cv2.INTER_AREA)
  
  return img

def render_frame(img):
  height, width = img.shape
  out = ""
  
  for y in range(height):
    for x in range(width):
      pixel = img[y,x]
              
      if pixel > 204:
        out += "██"
      elif pixel > 154:
        out += "▓▓"
      elif pixel > 102:
        out += "▒▒"
      elif pixel > 51:
        out += "░░"
      else:
        out += "  "
      
    out += "\n"

  return out[:-1]
