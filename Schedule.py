from asyncio import tasks
import Task
from Date import Date
import os
from utility.progress_bar import progressBar

class Schedule:
    def __init__(self):
        self._tasks = []
        
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
        
        names = [task.name for task in self._tasks] #Grabs all task names
        
        task_name = input("Input a new task name: ")
        while task_name in names or task_name == "ALL" or task_name.isnumeric() == True: #Checks if the name is already used, if the name is "ALL" (See view function), or if the name is only numbers
            if task_name in names: #Case if name has already been used
                task_name = input(f"The task name {task_name} has already been used, please input another task name: ")
            if task_name == "ALL": #Case if name is "ALL"
                task_name = input(f"The task name {task_name} can't be used, please input another task name: ")
            if task_name.isnumeric() == True: # Case if name is only numbers "ex: 1, 2332"
                task_name = input(f"The task name can't be all numbers, please input another task name: ")
        
        task_type = input("Input the task type: ")
        while task_type not in task_types.keys(): #Checks to see if the task type inputted is valid
            task_type = input(f"{task_type} is not a vaild task type. Please input a valid task type: ")
        task_category = task_types[task_type] #Saves what kind of task the task type is for later use
        task_date = input("Input the (start) date of the task: ")
        
        valid_date = False
        while (valid_date == False): #Trys to create a date object since that validates the input in it's initalization
            try:
                test_date = Date(task_date)
            except AssertionError: #Date was not in a valid format
                task_date = input(f"{task_date} is not a valid date, input a valid date: ")
            else: #Date is in a valid format and we can continue along
                valid_date = True
        valid_date = False #Resets to False in case we have a Recurring Task
        
        time_validation = True
        try: #This try catch makes sure the user inputted a float
            task_time = float(input("Please input the start time from 0.00 to 23.75: "))
        except:
            print("That was an invalid input type, setting time to -1: ")
            task_time = -1
            time_validation = False
        while 0 > task_time or task_time > 23.75 or time_validation==False: 
            try: #In case the user enters a string or char
                task_time = float(input(f"{task_time} is not a valid start time, please input a valid start time: "))
            except:
                print("That was an invalid input type")
                time_validation = False
                task_time = -1
            else:
                time_validation = True
       
        duration_validation = True
        try: #makes sure the duration is a valid float
             task_duration = float(input("Please input a duration between 0.25 and 23.75: "))
        except:
            print("That was an invalid input, setting duration to -1: ")
            task_duration = -1
            duration_validation = False
        while task_duration > 23.75 or task_duration < .25 or duration_validation==False: 
            try: #In case the user enters a string or char
                task_duration = float(input(f"{task_duration} is not a valid duration. Please input a number between .25 and 23.75: "))
            except:
                print("That was an invalid input type")
                duration_validation = False
                task_duration = -1
            else:
                duration_validation = True
        
        if task_category == "Recurring": #We got the task type earlier so now we create the correct one, in this case a Recurring task
            end_date= input("Input the end date of the task: ") #Recurring needs two more piece of info: end date and frequency
            while (valid_date == False): #Validates the date
                try:
                    test_date = Date(end_date)
                except AssertionError:
                    end_date = input(f"The {end_date} is not a valid date type, input a valid date: ")
                else:
                    if end_date < task_date:
                        end_date = input(f"The end date: {end_date} is less than the start date: {task_date}. Input a valid date: ")
                    else:
                        valid_date = True
            
            frequency_validation = True
            try: #Makes sure the frequency is valid
                frequency = int(input("Input how frequent the task should occur (1 == daily, 7== weekly): "))
            except:
                print("That is not a valid integer! setting frequency to -1")
                frequency = -1
                frequency_validation = False
            while (frequency != 1 and frequency != 7) or frequency_validation==False: #Also makes sure the user input a 1 or a 7
                try: #In case the user enters a string or char
                    frequency = int(input(f"{frequency} is not a valid frequency. Please input either 1 or 7: "))
                except:
                    print("That was an invalid input")
                    frequency_validation = False
                    frequency = -1
                else:
                    frequency_validation = True
            
            recurring_name = Task.Recurring(task_name, task_type, task_time, task_duration, task_date, end_date, frequency)
            if recurring_name.overlaps(self._tasks) == True:
                #print(f'{task_name} could not be added due to scheduling conflicts!')
                return
            else:
                self._tasks.append(recurring_name) #Adds the task to a list of all task objects
                #print(f"{task_name} has been added!")
                return
        
        elif task_category == "Anti":
            anti_name = Task.Anti(task_name, task_type, task_time, task_duration, task_date)
            if anti_name.overlaps(self._tasks) == False:
                #print(f'{task_name} could not be added because the Recurring Task does not exist, or an Anti Task is already added for that time!')
                return
            else:
                self._tasks.append(anti_name) #Adds the task to a list of all task objects
                #print(f"{task_name} has been added!")
                return
       
        else: #Task would have to be a Transient task
            transient_name = Task.Transient(task_name, task_type, task_time, task_duration, task_date)
            if transient_name.overlaps(self._tasks) == True:
                #print(f'{task_name} could not be added due to scheduling conflicts!')
                return
            else:
                self._tasks.append(transient_name) #Adds the task to a list of all task objects
                #print(f"{task_name} has been added!")
                return
    
    def view(self):
        '''Allows the user to specify the name of a task, and will display the contents of that task if it exists.'''
        # Prompt user for task name.
        name = input("Task name? >> ")
        
        # Edge case:
        # Display all the tasks in a user-friendly way, if asked to.
        if name == 'ALL':
            for index, task in enumerate(self._tasks):
                print(f'[{index}] [{task.__class__.__name__[0]}] {task.name}')
            return
        
        # Search for a task with the given task name, and if found, display its contents.
        for index, item in enumerate(progressBar(self._tasks, prefix=f'Searching')):
            if (item.name == name) or (str(index) == name): 
                print(f'Searching\nSearch stopped: task \'{name}\' found\n')
                self._tasks[index].view()
                return
            
        # Fallback message if no task could be found with the given name.
        print(f'Sorry, no task with the name \'{name}\' currently exists.')
    
    def delete(self):
        '''Allows the user to delete a task using a task name.'''
        # Prompt user for task name.
        name = input("Task name? >> ")
        
        # Search for a task with the given task name, and if found, delete it from the schedule.
        for index, item in enumerate(progressBar(self._tasks, prefix=f'Searching')):
            if item.name == name:
                print(f'Searching\nSearch stopped: task \'{name}\' found\n')
                self._tasks.pop(index)
                print(f'Deleted task \'{name}\'')
                return
            
        # Fallback message if no task could be found with the given name.
        print(f'Sorry, no task with the name \'{name}\' currently exists.')

    def edit(self):
        task_name = input("Input a new task name:")
        while task_name not in [task.name for task in self._tasks]:
            input("That task name is not in the schedule, please input a task in the schedule: ")
        else: 
            pass

    def view_day(self):
        day_input = Date(input('Enter the date you would like to view: '))
        dayView = Schedule()
        
        #day_list = [task for task in self._tasks if task.date == day_input]


        
        # for task in self._tasks: 
        #     if isinstance(task, Task.Transient):
        #         if task.date == day_input:
        #             day_list.append(task)
            

        #     if isinstance(task, Task.Recurring):
        #         current_day = task.start_date
        #         while current_day <= day_input:
        #             if current_day == day_input:
        #                 #Then check if antitask cancels out instance of recurring task
        #                 for anti_task in self._tasks:
        #                     if isinstance(anti_task, Task.Anti):
        #                         if anti_task.start_time != task.start_time and anti_task.duration != task.duration:
        #                             day_list.append(task)
        #                             #If the Anti Task does not cancel the instance on this day, append it to the list
                                
                                   
        #         current_day = current_day.plus(task.frequency)
        
        #Sort the list by earliest time to latest time
        #day_list.sort(key=task.start_time)

        #Display list
        if day_list:
            print(f'{day_list}') #Will fix the formatting
        else:
            print(f'There are no tasks scheduled for {day_input.pretty()}')
            
        

    def view_week(self):
        pass

    def view_month(self):
        pass
    

# -----------------------------------
schedule = Schedule() # This effectively acts as a singleton.
