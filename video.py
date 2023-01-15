#module for video processing

import cv2

def extract_video(path):
  capture = cv2.VideoCapture(path)
  success = True

  while success:
    success, img = capture.read()
    
    if success:
      yield img
    
def process_frame(img, height):
  #img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  
  ratio = height / img.shape[0]
  newsize = round(img.shape[0]*ratio), round(img.shape[1]*ratio)
  
  img = cv2.resize(img, newsize, interpolation=cv2.INTER_AREA)
  
  return img

def render_frame(img):
  height, width, channels = img.shape
  out = ""
  
  for y in range(height):
    for x in range(width):
      pixel = img[y,x][0]
              
      if pixel > 204:
        out += "███"
      elif pixel > 154:
        out += "▓▓▓"
      elif pixel > 102:
        out += "▒▒▒"
      elif pixel > 51:
        out += "░░░"
      else:
        out += "   "
      
    out += "\n"
  
  return out[:-1]
