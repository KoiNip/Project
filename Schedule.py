import Task
import os


class Schedule:
    _tasks = []
    _task_type_names = {
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
        
    
    def add_task(self):
        names = [task.name for task in self._tasks]
        
        task_name = input("Input a new task name:")
        while task_name in names:
            input("That task name has already been used, please input another task name: ")
        task_type = input("Input the task type: ")
        while task_type not in self._task_type_names.keys():
            input("That is not a vaild task type. Please input a valid task type: ")
        task_type = self._task_type_names[task_type]
        input("Input the ")
        

        pass
        

    
    def delete(self):
        pass

    def edit(self):
        names = [task.name for task in self._tasks]
        task_name = input("Input a new task name:")
        while task_name not in names:
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
            
        pass

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