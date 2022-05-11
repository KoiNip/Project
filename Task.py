from tracemalloc import start
from Date import Date
import Schedule
import json
import math

class Task:
    task_types = [
        'Class',
        'Study',
        'Sleep',
        'Exercise',
        'Work',
        'Meal',
        'Visit',
        'Shopping',
        'Appointment',
        'Cancellation'
    ]

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

    def serialize(self):
        class_name = self.__class__.__name__
        
        if class_name == 'Recurring': return Recurring.serialize(self)
        if class_name == 'Transient': return Transient.serialize(self)
        if class_name == 'Anti': return Anti.serialize(self)

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
        
    def all_days_as_list(self):
        result = []
        
        dates = 'something here'
        
        for index, d in enumerate(dates):
            temporary_task = Recurring(
                name=f'{self.name}_TEMP_{index}',
                category=self.type,
                start_time=self.start_time,
                duration=self.duration,
                start_date=d,
                end_date=self.end_date,
                frequency=self.frequency
            )
            result.append(temporary_task)
        
        return result
    
    def serialize(self):
        # result = super().serialize()
        result = super().__dict__.copy()
        result.update({
            "start_date": self.start_date.serialize(),
            "end_date": self.end_date.serialize(),
            "frequency": self.frequency
        })
        return result

    def overlaps(self, other):
        '''Checks if new task overlaps with current tasks in the schedule'''
        # Comparing Transient Task against Recurring Task
        # check if the transient task occurs with the recurring task start date or recurring task plus 7.....
        # if its on one of those days, check if the times are the same or occurs within the duration of recurring task

        # Comparing Transient Task against Transient Task
        # check if the dates are the same
        # if they're the same, check the times of the tasks and the durations for overlap

        # Comparing Transient Task against Anti Task
        # check if the anti task occurs on the same date as transient task
        # if dates are the same, check the time frame, if they overlap return False and create task

        #Creating new lists of each task type to iterate through
        transient_list = [other for other in Schedule.schedule._tasks if isinstance(other, Transient)]
        recurring_list = [other for other in Schedule.schedule._tasks if isinstance(other, Recurring)]
        anti_list = [other for other in Schedule.schedule._tasks if isinstance(other, Anti)]

        #iterate through transient list first
        for task in transient_list:
            end_time = task.start_time + task.duration #Time window a task occurs
           # self_end_time = self.start_time + self.duration
            self_current_day = self.start_date #Used to count each occurrence of a recurring task

            #Run the loop until the task reaches the final date in its lifetime
            #If the new recurring task occurs on the same day as a transient task at the same time, return True for overlap
            while(self_current_day <= self.end_date):
                if self.start_date == task.date:
                    if (task.start_time <= self.start_time <= end_time):
                        return True
                self_current_day = self.start_date.plus(self.frequency)

        #Iterate through the recurring list
        for task in recurring_list:
            end_time = task.start_time + task.duration
            self_end_time = self.start_time + self.duration
            current_day = task.start_date
            self_current_day = self.start_date
            #if frequency of task is daily, check if self is within task start and end date, if it is check the time, if not it passes this check
            if self.frequency == 1:
                if self.start_date <= task.start_date <= self.end_date: 
                    if (task.start_time <= self.start_time <= end_time):
                        return True
            #If frequency is weekly   
            elif self.frequency == 7:
                if self.start_date == task.start_date:
                    if (task.start_time <= self.start_time <= end_time):
                        return True
                elif self.start_date < task.start_date:
                    while(self_current_day <= task.end_date):
                        if self_current_day == task.start_date:
                            if (task.start_time <= self.start_time <= end_time):
                                return True
                        self_current_day = self.start_date.plus(self.frequency)
                elif self.start_date > task.start_date:
                    while(current_day <= self.start_date):
                        if current_day == self.start_date:
                            if (task.start_time <= self.start_time <= end_time):
                                return True
                        current_day = task.start_date.plus(task.frequency)
            return False   

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
        
    def serialize(self):
        # result = super().serialize()
        result = super().__dict__.copy()
        result.update({
            "date": self.date.serialize()
        })
        return result
    
    def overlaps(self, other):
        '''Checks if new task overlaps with current tasks in the schedule'''
        # Comparing Transient Task against Recurring Task
        # check if the transient task occurs with the recurring task start date or recurring task plus 7.....
        # if its on one of those days, check if the times are the same or occurs within the duration of recurring task

        # Comparing Transient Task against Transient Task
        # check if the dates are the same
        # if they're the same, check the times of the tasks and the durations for overlap

        # Comparing Transient Task against Anti Task
        # check if the anti task occurs on the same date as transient task
        # if dates are the same, check the time frame, if they overlap return False and create task

        transient_list = [other for other in Schedule.schedule._tasks if isinstance(other, Transient)]
        recurring_list = [other for other in Schedule.schedule._tasks if isinstance(other, Recurring)]
        anti_list = [other for other in Schedule.schedule._tasks if isinstance(other, Anti)]

        for task in transient_list:
            end_time = task.start_time + task.duration
            if self.date == task.date:
                if (task.start_time <= self.start_time <= end_time):
                    return True

        for task in recurring_list:
            end_time = task.start_time + task.duration
            
            current_day = task.start_date
            while (current_day <= task.end_date):
                if self.date == current_day:
                    if (task.start_time <= self.start_time <= end_time):
                        #check anti_list for valid anti task canceling one day of task
                        for anti in anti_list:
                            anti_end_time = anti.start_time + anti.duration
                            if self.date == anti.date:
                                if (anti.start_time <= self.start_time <= anti_end_time):
                                    return False
                        return True
                current_day = current_day.plus(task.frequency)
        #If no tasks in the schedule overlap, return false       
        return False

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
        
    def serialize(self):
        # result = super().serialize()
        result = super().__dict__.copy()
        result.update({
            "date": self.date.serialize()
        })
        return result
        
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