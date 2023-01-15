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

#gets a list of trending users
def get_users():
  users_url = "https://github.com/trending/developers?since=daily"
  r = requests.get(users_url)

  users_regex = r'alt="@(.*?)"'
  return re.findall(users_regex, r.text)

#download graph data for years 0000-9999
def download_year_data(threads=10):
  url_template = "http://github.com/users/{user}/contributions?from={year}-01-01"  
  year_queue = list(range(10000))
  output = {}

  print("Downloading proxies...")
  proxies = get_proxies()
  print("Downloading users...")
  users = get_users()
  print("Starting scraper...")
  
  def download_thread():
    current_proxy = random.choice(proxies)
    
    while len(year_queue) > 0:
      year = year_queue.pop(0) 
      year_string = format(year, '04d')
      
      url = url_template.format(year=year_string, user=random.choice(users))
      try:
        r = requests.get(url, proxies={"http": current_proxy}, timeout=4)
        if r.status_code != 200:
          print(f"Request failed with status code {r.status_code}")
          raise KeyError()
      except:
        year_queue.insert(0, year)
        current_proxy = random.choice(proxies)
        continue
      
      cols_regex = r'<g transform="translate\(\d+, \d+\)">(.*?)<\/g>'
      days_regex = r'data-date="(\d{4}-\d{2}-\d{2})"'
      
      try:
        cols_str = re.findall(cols_regex, r.text, flags=re.S)
        first_day = re.findall(days_regex, cols_str[0])[0]
        last_day = re.findall(days_regex, cols_str[-1])[-1]
        
        cols = []
        for col_str in cols_str:
          days = re.findall(days_regex, col_str)
          cols.append(days)
        
        print(f"Year: {year} | Start: {first_day} | End: {last_day}")
        output[year] = cols
      except IndexError:
        year_queue.insert(0, year)
        current_proxy = random.choice(proxies)
    
  for i in range(threads):
    thread = threading.Thread(target=download_thread, daemon=True)
    thread.start()
  
  while len(year_queue) > 0:
    try:
      time.sleep(1)
    except KeyboardInterrupt:
      break
  
  print("Done downloading.")
  return output

def write_graph_data(data, outfile="graph.csv"):  
  keys = list(data.keys())
  keys = sorted(keys)
  
  with open(outfile, "w") as f:
    writer = csv.writer(f)
    for key in keys:
      value = data[key]
      writer.writerow((key, value[0][0], value[-1][-1]))

if __name__ == "__main__":
  data = download_year_data()
  write_graph_data(data)