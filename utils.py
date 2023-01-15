#misc utilities

from datetime import date, timedelta
from contextlib import contextmanager
import csv
import os

year_data = {}

#context manager to change back to original directory
#https://stackoverflow.com/a/37996581
@contextmanager
def change_dir(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

def read_year_data(path="graph.csv"):
  with open(path) as f:
    reader = csv.reader(f)
    for row in reader:
      year = int(row[0])
      start_date = date(*list(map(int, row[1].split("-"))))
      end_date = date(*list(map(int, row[2].split("-"))))
      
      year_data[year] = (start_date, end_date)
      
  return year_data

#get dates for each column of the frame
def get_frame_dates(year):
  year_start = year_data[year][0]
  sundays = []
  for i in range(0, 51):
    sundays.append(year_start)
    year_start += timedelta(days=7)
    
  frame = []
  for column_start in sundays:
    column = []
    for i in range(0, 7):
      day = column_start + timedelta(days=i)
      column.append(day)
    frame.append(column)

  return frame