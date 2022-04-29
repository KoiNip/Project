from Date import Date

class Task:
    task_types = []
    json = {}

    def __init__(self, name, category, start_time, duration):
        self.name = name
        self.category = category
        self.start_time = round(start_time*4)/4
        self.duration = round(duration*4)/4

        # Parameter validation
        if not (0 <= self.start_time <= 23.75): 
            raise AssertionError('start_time must be a positive number from 0 (midnight) to 23.75 (11:45 pm)')
        if not (0.25 <= self.duration <= 23.75): 
            raise AssertionError('duration must be a positive number from 0.25 to 23.75')
        if self.category not in self.task_types: 
            raise AssertionError(f'{self.__class__.__name__} Tasks must have a category attribute of one of the following: {self.task_types}')

    # Make sure that the 'Task' superclass cannot be instantiated.
    def __new__(cls, *args, **kwargs):
        if cls is Task:
            raise TypeError(f"only children of '{cls.__name__}' may be instantiated")
        return super().__new__(cls)
    
class Recurring(Task):
    task_types = [
        'Class',
        'Study',
        'Sleep',
        'Exercise',
        'Work',
        'Meal'
    ]

    def __init__(self, name, category, start_time, duration, start_date, end_date, frequency):
        super().__init__(name, category, start_time, duration)
        self.start_date = Date(start_date)
        self.end_date = Date(end_date)
        self.frequency = frequency

        # Parameter validation
        if self.frequency not in [1, 7]: raise AssertionError('frequency must be either 1 (daily) or 7 (weekly)')

    def to_json(self):
        self.json.update(
            {
                "Name" : self.name,
                "Type" : self.category,
                "StartDate" : self.start_date._date,
                "StartTime" : self.start_time,
                "Duration": self.duration,
                "EndDate" : self.end_date,
                "Frequency" : self.frequency
            }
        )
        return self.json

        
class Transient(Task):
    task_types = [
        'Visit',
        'Shopping',
        'Appointment'
    ]

    def __init__(self, name, category, start_time, duration, date):
        super().__init__(name, category, start_time, duration)
        self.date = Date(date)

class Anti(Task):
    task_types = [
        'Cancellation'
    ]

    def __init__(self, name, category, start_time, duration, date):
        super().__init__(name, category, start_time, duration)
        self.date = Date(date)