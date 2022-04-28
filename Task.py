from Date import Date
import operator


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