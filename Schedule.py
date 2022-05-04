import Task
import os


class Schedule:
    _tasks = []
        
    def add_task(self):
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
        
        task_name = input("Input a new task name:")
        while task_name in [task.name for task in self._tasks]:
            input("That task name has already been used, please input another task name: ")
        task_type = input("Input the task type: ")
        while task_type not in task_types.keys():
            input("That is not a vaild task type. Please input a valid task type: ")
        task_type = self._task_type_names[task_type]
        input("Input the ")
    
    def view(self):
        pass
    
    def delete(self):
        pass

    def edit(self):
        task_name = input("Input a new task name:")
        while task_name not in [task.name for task in self._tasks]:
            input("That task name is not in the schedule, please input a task in the schedule: ")
        else: 
            pass

    def read(self):
        file_name = input("Input the name of the file: ")
        while file_name not in self._tasks: #i dont think this will work
            input("File does not exist, enter a valid file name: ")
        else:
            
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