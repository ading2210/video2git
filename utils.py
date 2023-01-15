#misc utilities

from datetime import date, timedelta

#get all sundays in a year
def get_sundays(year):
  day = date(year, 1, 1)
  day += timedelta(days = 6-day.weekday())
  
  sundays = []
  while day.year == year:
    sundays.append(day)
    day += timedelta(days=7)
  
  return sundays

#get drawable screen
def get_drawable_screen(year):
  sundays = get_sundays(year)
  if sundays[0].day <= 4:
    del sundays[0]
  if 31 - sundays[-1].day >= 7:
    del sundays[-1]