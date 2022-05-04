from pickle import FALSE, TRUE
import Task
from Date import Date
import os
from utility.progress_bar import progressBar

class Schedule:
    _tasks = []
        
    def add_task(self):
        '''
        I added a sort of 'easter egg'
        in the view() function. Because of this,
        DO NOT ALLOW a task with the name 'ALL'
        to be accepted, and 
        DO NOT ALLOW a task name that is just numbers
        to be accepted. Thanks -Seth
        '''
        
        task_types = {
            'Class': 'Recurring',
            'Study': 'Recurring',
            'Sleep': 'Recurring',
            'Exercise': 'Recurring',
            'Work': 'Recurring',
            'Meal': 'Recurring',
            'Visit': 'Transient',
            'Shopping': 'Transient',
            'Appointment': 'Transient',
            'Cancellation': 'Anti'
        }
        
        names = [task.name for task in self._tasks]
        task_name = input("Input a new task name:")
        while task_name in names or task_name == "ALL" or task_name.isnumeric() == True:
            if task_name in names:
                task_name = input(f"The task name {task_name} has already been used, please input another task name: ")
            if task_name == "ALL":
                task_name = input(f"The task name {task_name} can't be used, please input another task name: ")
            if task_name.isnumeric() == True:
                task_name = input(f"The task name can't be all numbers, please input another task name: ")
        task_type = input("Input the task type: ")
        while task_type not in task_types.keys():
            task_type = input(f"{task_type} is not a vaild task type. Please input a valid task type: ")
        task_category = task_types[task_type]
        task_date = int(input("Input the (start) date of the task"))
        valid_date = FALSE
        while (valid_date == FALSE):
            try:
                test_date = Date(task_date)
            except AssertionError:
                task_date = int(input(f"{task_date} is not a valid date, input a valid date: "))
            else:
                valid_date = TRUE
        valid_date = FALSE
        task_time = float(input("Please input the start time to the nearest quarter (:15 = .25, :30 = .5, :45 = .75, :00 = .00):"))
        while 0 > task_time or task_time > 24 or task_time % .25 != 0: 
            task_time = float(input(f"{task_time} is not a valid start time, please input a valid start time"))
        task_duration = float(input("Please input the duration to the nearest quarter (:15 = .25, :30 = .5, :45 = .75, :00 = .00)"))
        while task_duration > 23.75 or task_duration < .25 or task_duration % .25 != 0:
            task_duration = float(input(f"{task_duration} is not a valid duration. Please input a rounded number between .25 and 23.75: "))
        if task_category == "Recurring":
            end_date= int(input("Input the end date of the task: "))
            while (valid_date == FALSE):
                try:
                    test_date = Date(end_date)
                except AssertionError:
                    task_date = int(input(f"{end_date} is not a valid date, input a valid date: "))
                else:
                    valid_date = TRUE
            frequency = int(input("Input how frequent the task should occur (1 == daily, 7== weekly): "))
            while frequency > 7 and frequency < 1:
                frequency = int(input(f"{frequency} is not a vaild frequency, please input a number from 1 to 7"))
            #add overlap here when function finished
            recurring_name = Task.Recurring(task_name, task_type, task_time, task_duration, task_date, end_date, frequency)
            self._tasks.append(recurring_name)
            print(f"{task_name} has been added!")
            return
        elif task_category == "Anti":
            #add overlap here when function finished
            anti_name = Task.Anti(task_name, task_type, task_time, task_duration, task_date)
            self._tasks.append(anti_name)
            print(f"{task_name} has been added!")
            return
        else:
            #add overlap here when function is finished
            transient_name = Task.Transient(task_name, task_type, task_time, task_duration, task_date)
            self._tasks.append(transient_name)
            print(f"{task_name} has been added!")
            return
    
    def view(self):
        name = input("Task name? >> ")
        
        # EASTER EGG
        if name == 'ALL':
            for index, task in enumerate(self._tasks):
                print(f'[{index}] [{task.__class__.__name__[0]}] {task.name}')
            return
        
        for index, item in enumerate(progressBar(self._tasks, prefix=f'Searching')):
            if (item.name == name) or (str(index) == name): 
                print(f'Searching\nSearch stopped: task \'{name}\' found\n')
                self._tasks[index].view()
                return
            
        print(f'Sorry, no task with the name \'{name}\' currently exists.')
    
    def delete(self):
        name = input("Task name? >> ")
        
        for index, item in enumerate(progressBar(self._tasks, prefix=f'Searching')):
            if item.name == name:
                print(f'Searching\nSearch stopped: task \'{name}\' found\n')
                self._tasks.pop(index)
                print(f'Deleted task \'{name}\'')
                return
            
        print(f'Sorry, no task with the name \'{name}\' currently exists.')

    def edit(self):
        task_name = input("Input a new task name:")
        while task_name not in [task.name for task in self._tasks]:
            input("That task name is not in the schedule, please input a task in the schedule: ")
        else: 
            pass

    def read(self):
        file_name = input("Input the name of the file: ")
        if os.path.exist("{file_name}"):
            f = open("{file_name}", "awt")
        else:
            print("The file {file_name} is not a valid file")

    def write(self):
        file_name = input("Input the name of the file: ")
        while file_name not in self._tasks:
            input("File does not exist, enter a valid file name: ")
        else: 
            pass

    def write_day(self):
        pass

    def write_week(self):
        pass

    def write_month(self):
        pass

    def view_day(self):
        pass

    def view_week(self):
        pass

    def view_month(self):
        pass
    

# -----------------------------------
schedule = Schedule()