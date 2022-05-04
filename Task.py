from Date import Date
import json
import math

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
        def pretty_time(time):
            mapping = {.0: '00', .25: '15', .5: '30', .75: '45'}
            minutes, hour = math.modf(time)

            period = 'AM' if hour <= 11 else 'PM'
            hour = 12 if (hour == 0 or hour == 12) else int(hour) % 12
            minutes = mapping[minutes]

            return f'{hour}:{minutes} {period}'
        
        duration_map = {
            .25: '15',
            .5: '30',
            .75: '45'
        }
        
        title = f'{self.name} [{self.__class__.__name__}] [{self.type}]'
        print(f'{title}\n{"-"*len(title)}')
        
        if (self.duration not in duration_map):
            better_duration = f'{self.duration} hours'
        else:
            better_duration = f'{duration_map[self.duration]} minutes'
        
        sub_title = f'Starts at {pretty_time(self.start_time)} and lasts for {better_duration}'
        print(sub_title)
    
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
        true_freq = 'Daily' if self.frequency == 1 else 'Weekly'
        print(f'Starts on {self.start_date.pretty()} and ends on {self.end_date.pretty()}\nFrequency: {true_freq}')
        
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
        print(f'Scheduled for {self.date.pretty()}')

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
        print(f'Occurs on {self.date.pretty()}')
        
if __name__ == '__main__':
    test_recurring = Recurring(
        name='catching some zzz',
        category='Sleep',
        start_time=22.5,
        duration=8,
        start_date=20220503,
        end_date=20221231,
        frequency=1
    )
    test_recurring.view()
    print()
    
    test_transient = Transient(
        name = 'Go gym',
        category = 'Visit',
        start_time = 9.5,
        duration=2,
        date=20220509
    )
    test_transient.view()
    print()
    
    test_anti = Anti(
        name='I really didn\'t want to walk',
        category='Cancellation',
        date=20200415,
        start_time=10.25,
        duration=0.75
    )
    test_anti.view()
    print()