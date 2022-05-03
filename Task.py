from Date import Date
import json

class Task:
    task_types = []

    def __init__(self, name, category, start_time, duration):
        self.name = name
        self.type = category
        self.start_time = round(start_time*4)/4
        self.duration = round(duration*4)/4

        # Parameter validation
        if not (0 <= self.start_time <= 23.75): 
            raise AssertionError('start_time must be a positive number from 0 (midnight) to 23.75 (11:45 pm)')
        if not (0.25 <= self.duration <= 23.75): 
            raise AssertionError('duration must be a positive number from 0.25 to 23.75')
        if self.type not in self.task_types: 
            raise AssertionError(f'{self.__class__.__name__} Tasks must have a category attribute of one of the following: {self.task_types}')

    # Make sure that the 'Task' superclass cannot be instantiated.
    def __new__(cls, *args, **kwargs):
        if cls is Task:
            raise TypeError(f"only children of '{cls.__name__}' may be instantiated")
        return super().__new__(cls)

    def overlaps(self, other):
        '''Returns True if self overlaps other, otherwise False.'''
        pass
    
    def to_json(self):
        '''Returns a JSON string representation of the task.
        Useful for writing schedules to a file.
        '''
        return (json.dumps(self.__dict__, default=Date.as_int, indent="\t"))

    def view(self):
        '''Prints a user-friendly representation of the task.'''
        title = f'{self.name} [{self.__class__.__name__}]'
        print(f'{title}\n{"-"*len(title)}')
        print()
    
class Recurring(Task):
    '''Reucrring tasks occur daily or weekly.'''
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
        
    def view(self):
        super().view()
        print('something else here')
        
class Transient(Task):
    '''Transient tasks only occur once.'''
    task_types = [
        'Visit',
        'Shopping',
        'Appointment'
    ]

    def __init__(self, name, category, start_time, duration, date):
        super().__init__(name, category, start_time, duration)
        self.date = Date(date)
        
    def view(self):
        super().view()
        print('something else here')

class Anti(Task):
    '''Anti-tasks are used to cancel out one repetition of a recurring task.

    Consequently, there must be a recurring task that is scheduled for the given
    date, and that recurring task must have a start time that matches the start
    time of this anti-task. Similarly, the durations of the task and anti-task must be
    the same.'''
    task_types = [
        'Cancellation'
    ]

    def __init__(self, name, category, start_time, duration, date):
        super().__init__(name, category, start_time, duration)
        self.date = Date(date)
        
    def view(self):
        super().view()
        print('something else here')