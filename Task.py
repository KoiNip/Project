from Date import Date
import Schedule
import math

class Task:
    '''Represents the functionality of a generic Task object.'''
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
        '''Returns a JSON serializable form of a Task instance.'''
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
    
    def serialize(self):
        result = super().__dict__.copy()
        result.pop('start_date')
        result.pop('end_date')
        
        result.update({
            "Name": result.pop('name'),
            "Type": result.pop('type'),
            "StartTime": result.pop('start_time'),
            "Duration": result.pop('duration'),
            "StartDate": self.start_date.serialize(),
            "EndDate": self.end_date.serialize(),
            "Frequency": result.pop('frequency')
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

        self_end_time = self.start_time + self.duration

        #Iterate through transient list first
        for task in transient_list:
            end_time = task.start_time + task.duration #Time window a task occurs
            self_current_day = self.start_date #Used to count each occurrence of a recurring task

            #Run the loop until the task reaches the final date in its lifetime
            #If the new recurring task occurs on the same day as a transient task at the same time, return True for overlap
            while self_current_day <= self.end_date:
                if self.start_date == task.date:
                    if (task.start_time <= self.start_time < end_time) or (task.start_time <= self_end_time <= end_time):
                        print(f'{self.name} could not be added to the schedule because the task, {task.name}, is already happening at that time!')
                        return True
                self_current_day = self.start_date.plus(self.frequency)

        #Iterate through the recurring list
        for task in recurring_list:
            end_time = task.start_time + task.duration
            current_day = task.start_date
            self_current_day = self.start_date
            #if frequency of task is daily, check if self is within task start and end date, if it is check the time, if not it passes this check
            if self.frequency == 1 or task.frequency == 1:
                if self.start_date <= task.start_date <= self.end_date:
                    if (task.start_time <= self.start_time < end_time) or (task.start_time <= self_end_time <= end_time):
                        print(f'{self.name} could not be added to the schedule because the task, {task.name}, is already happening at that time!')
                        return True
                elif task.start_date <= self.start_date <= task.end_date:
                  if (task.start_time <= self.start_time < end_time) or (task.start_time <= self_end_time <= end_time):
                        print(f'{self.name} could not be added to the schedule because the task, {task.name}, is already happening at that time!')
                        return True
            #If frequency is weekly
            elif self.frequency == 7 or task.frequency == 7:
                if self.start_date == task.start_date:
                    if (task.start_time <= self.start_time < end_time) or (task.start_time <= self_end_time <= end_time):
                        print(f'{self.name} could not be added to the schedule because the task, {task.name}, is already happening at that time!')
                        return True
                elif self.start_date < task.start_date:
                    if self.end_date > task.start_date:
                        while self_current_day <= task.start_date:
                            if self_current_day == task.start_date:
                                if (task.start_time <= self.start_time < end_time) or (task.start_time <= self_end_time <= end_time):
                                    print(f'{self.name} could not be added to the schedule because the task, {task.name}, is already happening at that time!')
                                    return True
                            self_current_day = self.start_date.plus(self.frequency)
                elif self.start_date > task.start_date:
                    while current_day <= self.start_date:
                        if current_day == self.start_date:
                            if (task.start_time <= self.start_time < end_time) or (task.start_time <= self_end_time <= end_time):
                                print(f'{self.name} could not be added to the schedule because the task, {task.name}, is already happening at that time!')
                                return True
                        current_day = task.start_date.plus(task.frequency)
        print(f'{self.name} has been successfully added to the schedule!')
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
        result = super().__dict__.copy()
        result.pop('date')
        
        result.update({
            "Name": result.pop('name'),
            "Type": result.pop('type'),
            "StartTime": result.pop('start_time'),
            "Duration": result.pop('duration'),
            "Date": self.date.serialize()
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

        self_end_time = self.start_time + self.duration

        for task in transient_list:
            end_time = task.start_time + task.duration
            if self.date == task.date:
                if (task.start_time <= self.start_time < end_time) or (task.start_time <= self_end_time <= end_time):
                    print(f'{self.name} could not be added to the schedule because the task, {task.name}, is already happening at that time!')
                    return True

        for task in recurring_list:
            end_time = task.start_time + task.duration
            
            current_day = task.start_date
            while (current_day <= task.end_date):
                if self.date == current_day:
                    if (task.start_time <= self.start_time < end_time) or (task.start_time <= self_end_time <= end_time):
                        #check anti_list for valid anti task canceling one instance of task
                        for anti in anti_list:
                            anti_end_time = anti.start_time + anti.duration
                            if self.date == anti.date:
                                if (anti.start_time <= self.start_time <= anti_end_time) or (anti.start_time <= self_end_time <= end_time):
                                    print(f'{self.name} has been successfully added to the schedule!')
                                    return False
                        print(f'{self.name} could not be added to the schedule because the task, {task.name}, is already happening at that time!')
                        return True
                current_day = current_day.plus(task.frequency)
        #If no tasks in the schedule overlap, return false     
        print(f'{self.name} has been successfully added to the schedule!')  
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
        result = super().__dict__.copy()
        result.pop('date')
        
        result.update({
            "Name": result.pop('name'),
            "Type": result.pop('type'),
            "StartTime": result.pop('start_time'),
            "Duration": result.pop('duration'),
            "Date": self.date.serialize()
        })
        return result

    #Anti overlap checks if the entered task falls on the same day and time as an instance of a recurring task
    def overlaps(self, other):

        recurring_list = [other for other in Schedule.schedule._tasks if isinstance(other, Recurring)]
        anti_list = [other for other in Schedule.schedule._tasks if isinstance(other, Anti)]


        #Check if Anti Task exists first
        for task in anti_list:
            if self.date == task.date:
                if self.start_time == task.start_time and self.duration == task.duration:
                    print(f'{self.name} can not be added because {task.name} is already cancelling a task at that time!')
                    return False #Anti Task is already being used at the entered Date and Time/Duration

        for task in recurring_list:
            current_day = task.start_date
            
            while current_day <= task.end_date:
                if self.date == current_day:
                    if self.start_time == task.start_time and self.duration == task.duration:
                        print(f'{self.name} has successfully cancelled out {task.name} at {self.start_time} on {self.date.pretty}!')
                        return True #A True return means that a valid recurring instance exists and can be cancelled out
                current_day = current_day.plus(task.frequency)
        print(f'There were no tasks in the schedule for {self.name} to cancel out!')
        return False #A false return means that there were no recurring tasks in the schedule that could be cancelled
        
if __name__ == '__main__':
    pass
