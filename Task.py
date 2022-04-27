from dataclasses import dataclass
import operator

class Date:
    year = {
        '01': {'name': 'January', 'days': 31},
        '02': {'name': 'February', 'days': 28},
        '03': {'name': 'March', 'days': 31},
        '04': {'name': 'April', 'days': 30},
        '05': {'name': 'May', 'days': 31},
        '06': {'name': 'June', 'days': 30},
        '07': {'name': 'July', 'days': 31},
        '08': {'name': 'August', 'days': 31},
        '09': {'name': 'September', 'days': 30},
        '10': {'name': 'October', 'days': 31},
        '11': {'name': 'November', 'days': 30},
        '12': {'name': 'December', 'days': 31},
    }
    
    def __init__(self, date):
        self.date = date
        
    date = property(operator.attrgetter('date'))
    @date.setter
    def date(self, d):
        if not len(d) == 8: raise TypeError("dates must be 8 digits long")
        year = d[:4], month = d[4:6], day = d[6:8]
        if not d.isdigit(): raise TypeError("dates must only contain integers")
        if not 1 <= month <= 12: raise TypeError("month value must range between 01 and 12")
        if not day <= self.year[month]["days"]: raise TypeError(f'month {month} can have at most {self.year[month]["days"]} days')
        self.date = d
        
    def pretty(self):
        year = self.date[:4]
        month = self.date[4:6]
        day = self.date[6:8]
            
        return f'{self.year[month]["name"]} {day}, {year}'
            
today = Date('20220427')
print(today.pretty())

class Task:    
    def __init__(self, name, start_time, duration):
        self.name = name
        self.start_time = start_time
        self.duration = duration
    
    start_time = property(operator.attrgetter('start_time'))
    @start_time.setter
    def start_time(self, s):
        if not (0 <= s <= 23.75): raise TypeError("start_time must be a positive number from 0 (midnight) to 23.75 (11:45 pm)")
        self.start_time = round(s, 0.25)
        
    duration = property(operator.attrgetter('duration'))
    @duration.setter
    def duration(self, d):
        if not (0.25 <= d <= 23.75): raise TypeError("duration must be a positive number from 0.25 to 23.75")
        self.duration = round(d, 0.25)
    
class Recurring(Task):
    def __init__(self, start_date, end_date, frequency):
        self.start_date = Date(start_date)
        self.end_date = Date(end_date)
        self.frequency = frequency
        
class Transient(Task):
    def __init__(self, date):
        self.date = Date(date)

class Anti(Task):
    def __init__(self, date):
        self.date = Date(date)