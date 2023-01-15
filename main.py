import cv2
import math
import os
import shutil
import time
import json

import video
import utils

def setup_repo(path):
  if (os.path.exists(path)):
    shutil.rmtree(path)
  os.mkdir(path)
  
  with utils.change_dir(path):
    os.system("git init -b main")

#todo: allow dates earlier than 1970 using https://stackoverflow.com/a/24977895
def commit_date(path, date, frame, commit, author):
  with utils.change_dir(path):
    commit_time_unix = int(time.mktime(date.timetuple()))
    commit_time = f"@{commit_time_unix} +0000"
    cmd = (
      f'GIT_AUTHOR_DATE="{commit_time}" GIT_COMMITTER_DATE="{commit_time}"',
      f'GIT_AUTHOR_NAME="{author["name"]}" GIT_AUTHOR_EMAIL="{author["email"]}"',
      f'GIT_COMMITTER_NAME="{author["name"]}" GIT_COMMITTER_EMAIL="{author["email"]}"',
      f'git commit --allow-empty -m "frame {frame}, commit {commit}"',
    )
    utils.run_cmd(" ".join(cmd), hide_output=True)

def main(repo_path, video_path, git_author):
  utils.read_year_data()
  
  setup_repo(repo_path)

  frame_count = 0
  commit_count = 0
  total_commits = 0
  with utils.change_dir(repo_path): 
    for frame, capture in video.extract_video(video_path):
      os.system("clear")

      img = video.process_frame(frame, height=7)
      img2 = video.process_frame(frame, height=14)
      height, width = img.shape
      
      print(video.render_frame(img2))
      print("-"*img2.shape[1]*2)
      print(video.render_frame(img))
      total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
      print(f"Frame: {frame_count}/{total_frames}")
      print(f"Commits (previous frame): {commit_count}")
      total_commits += commit_count
      print(f"Commits (total): {total_commits}")
      
      frame_dates = utils.get_frame_dates(frame_count+1970)
      commit_count = 0
      for x in range(width):
        for y in range(height):
          color = max(0, math.ceil(img[y,x]/51.2)-1)
          
          for i in range(color):
            date = frame_dates[x][y]
            commit_date(repo_path, date, frame_count, commit_count, git_author)
            
            commit_count += 1
      
      for i in range(5):
        date = frame_dates[-1][-1]
        commit_date(repo_path, date, frame_count, commit_count, git_author)
        commit_count += 1

      frame_count += 1

if __name__ == "__main__":
  with open("config.json") as f:
    config = json.loads(f.read())

  main(config["repo"], config["video"], config["author"])