import cv2
import math
import os
import shutil
import time

import video
import utils

def setup_repo(path):
  if (os.path.exists(path)):
    shutil.rmtree(path)
  os.mkdir(path)
  
  with utils.change_dir(path):
    os.system("git init -b main")

def commit_date(path, date, frame, commit):
  with utils.change_dir(path):
    commit_time = time.mktime(date.timetuple())
    with open(path+"/README", "w") as f:
      f.write("frame {frame}, commit {commit}")
      
    os.system("git add README")
    os.system(f'git commit -m "frame {frame}, commit {commit}" --date={commit_time}')

def main(repo_path):
  utils.read_year_data()
  
  setup_repo(repo_path)

  frame_count = 0
  with utils.change_dir(repo_path):
    for frame in video.extract_video("./input/bad_apple.webm"):
      os.system("clear")
      
      img = video.process_frame(frame, height=7)
      height, width = img.shape
      
      print(video.render_frame(img))
      print(f"Frame: {frame_count}")
      
      frame_dates = utils.get_frame_dates(frame_count+1)
      commit_count = 0
      for x in range(width):
        for y in range(height):
          color = max(0, math.ceil(img[y,x]/51.2)-1)
          
          for i in range(color):
            date = frame_dates[x][y]
            commit_date(repo_path, date, frame_count, commit_count)
            
            commit_count += 1
    frame_count += 1

if __name__ == "__main__":
  main("./repo")