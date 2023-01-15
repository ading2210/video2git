#module to scrape the github website

import threading
import requests
import time
import re
import csv
import random

#gets a list of working proxies
def get_proxies():
  proxies_url = "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt"
  r = requests.get(proxies_url)
  lines = r.text.split("\n")
  return lines

#gets a list of all trending users
def get_users():
  urls = [
    "https://github.com/trending/developers?since={time_period}",
    "https://github.com/trending?since={time_period}"
  ]
  users = []
  for url in urls:
    for time_period in ["daily", "weekly", "monthly"]:
      r = requests.get(url.format(time_period=time_period))

      users_regex = r'alt="@(.*?)"'
      users.extend(re.findall(users_regex, r.text))
  
  users = list(set(users))
  return users

#download graph data for years 0001-9999
#this downloads ~100MB of data and takes ~23 minutes on a fast internet connection
def download_graph_data(threads=10, verbose=False):
  url_template = "http://github.com/users/{user}/contributions?from={year}-01-01"  
  year_queue = list(range(1, 10000))
  output = {}

  print("Downloading proxies...")
  proxies = get_proxies()
  print("Downloading users...")
  users = get_users()
  if (len(users)) < 1:
    print("Could not download users.")
    return None
  print(f"Downloaded {len(users)} users.")
  
  def download_thread():
    current_proxy = random.choice(proxies)
    
    while len(year_queue) > 0:
      year = year_queue.pop(0) 
      year_string = format(year, '04d')
      
      user = user=random.choice(users)
      url = url_template.format(year=year_string, user=user)
      try:
        r = requests.get(url, proxies={"http": current_proxy}, timeout=4)
        if r.status_code == 404:
          del users[users.index(user)]
        elif r.status_code != 200:
          if verbose: print(f"Request failed with status code {r.status_code}")
          raise KeyError()
      except:
        year_queue.insert(0, year)
        current_proxy = random.choice(proxies)
        continue
      
      cols_regex = r'<g transform="translate\(\d+, \d+\)">(.*?)<\/g>'
      days_regex = r'data-date="(\d{4}-\d{2}-\d{2})"'
      
      try:
        cols_str = re.findall(cols_regex, r.text, flags=re.S)
        if len(cols_str) < 52:
          raise IndexError()
        
        cols = []
        for col_str in cols_str:
          days = re.findall(days_regex, col_str)
          cols.append(days)
          
        if verbose: 
          print(f"Year: {year_string} | Start: {cols[1][0]} | End: {cols[51][0]}")
        else: 
          finished_string = format(9999-len(year_queue), '04d')
          print(f"\rDownloaded {finished_string}/9999 years.", end="")
          
        output[year] = cols
      except IndexError:
        year_queue.insert(0, year)
        current_proxy = random.choice(proxies)
  
  print(f"Starting {threads} threads...")
  for i in range(threads):
    thread = threading.Thread(target=download_thread, daemon=True)
    thread.start()
  
  while len(year_queue) > 0:
    try:
      time.sleep(1)
    except KeyboardInterrupt:
      break
  
  print("\nDone downloading.")
  return output

#write the downloaded graph data to a csv file
def write_graph_data(data, outfile="graph.csv"):  
  keys = list(data.keys())
  keys = sorted(keys)
  
  with open(outfile, "w") as f:
    writer = csv.writer(f)
    for key in keys:
      value = data[key]
      writer.writerow((key, value[1][0], value[51][0]))

if __name__ == "__main__":
  start_time = time.time()
  data = download_graph_data(threads=20)
  write_graph_data(data)
  end_time = time.time()
  
  time_diff = end_time - start_time
  print(f"Finished in {round(time_diff/60, 2)} minutes")