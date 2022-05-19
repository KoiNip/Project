import json
from os.path import exists
from Schedule import Schedule, schedule
import Task
from Date import Date

class FileHandler():
    def read(self):
        '''Reads in a json formatted schedule from the ./schedules folder.'''
        # Get the correct file path, including .json extension
        file_name = input("File name to read from? >> ")
        if not file_name.endswith('.json'): file_name += '.json'
        file_path = f'./schedules/{file_name}'
        
        try:
            # Make sure file exists and can be opened properly.
            if not exists(file_path): raise FileNotFoundError
            with open(file_path) as infile:
                schedule_as_json = json.load(infile)
            
            # Setup work
            new_schedule = schedule._tasks.copy()
            task_types = {
                "Recurring": ['Class', 'Study', 'Sleep', 'Exercise', 'Work', 'Meal'],
                "Transient": ['Visit', 'Shopping', 'Appointment'],
                "Anti": ['Cancellation']
            }
            all_possible_task_types = [item for sublist in task_types.values() for item in sublist]
            generic_task_attributes = ['Name', 'Type', 'StartTime', 'Duration']
            
            # Dictionary to different task helper methods.
            def dict_to_recurring(dct):
                '''Accepts a dictionary as input, returns a Recurring Task object built from the dictionary, if possible.'''
                recurring_task_attributes = ['StartDate', 'EndDate', 'Frequency']
                recurring_task_attributes.extend(generic_task_attributes)
                for attribute in dct:
                    if attribute not in recurring_task_attributes: raise AttributeError

                return Task.Recurring(
                    dct['Name'], dct['Type'], 
                    dct['StartTime'], dct['Duration'], 
                    dct['StartDate'], dct['EndDate'], 
                    dct['Frequency'])
    
            def dict_to_transient(dct):
                '''Accepts a dictionary as input, returns a Transient Task object built from the dictionary, if possible.'''
                transient_task_attributes = ['Date']
                transient_task_attributes.extend(generic_task_attributes)
                for attribute in dct:
                    if attribute not in transient_task_attributes: raise AttributeError
                
                return Task.Transient(
                    dct['Name'], dct['Type'], 
                    dct['StartTime'], dct['Duration'], 
                    dct['Date'])
                
            def dict_to_anti(dct):
                '''Accepts a dictionary as input, returns an Anti Task object built from the dictionary, if possible.'''
                anti_task_attributes = ['Date']
                anti_task_attributes.extend(generic_task_attributes)
                for attribute in dct:
                    if attribute not in anti_task_attributes: raise AttributeError
                    
                return Task.Anti(
                    dct['Name'], dct['Type'],
                    dct['StartTime'], dct['Duration'],
                    dct['Date']
                )
            
            # Create a task object (Recurring, Transient, or Anti) for every dictionary object
            # within the schedule json file.
            for dct in schedule_as_json:
                if dct['Type'] not in all_possible_task_types: raise AttributeError
                
                if dct['Type'] in task_types['Recurring']:
                    temp_task = dict_to_recurring(dct)
                elif dct['Type'] in task_types['Transient']:
                    temp_task = dict_to_transient(dct)
                elif dct['Type'] in task_types['Anti']:
                    temp_task = dict_to_anti(dct)
                    
                if temp_task.overlaps(new_schedule): raise RuntimeError
                new_schedule.append(temp_task)
                    
        except json.JSONDecodeError:
            print(f'File \'{file_path}\' contains invalid JSON or is corrupted.')
        except FileNotFoundError:
            print(f'File \'{file_path}\' does not exist.')
        except AttributeError:
            print(f'AttributeError: dict type could not be converted into a Recurring, Transient, or Anti Task.')
            print(f'{dct = }')
        except RuntimeError:
            print(f'One or more tasks in \'{file_path}\' overlaps with the current schedule. File reading is being terminated, and no changes to the schedule have been made.')
            return
        else:
            schedule._tasks = new_schedule
            print(f'Schedule loaded from \'{file_path}\' successfully!')
    
    def write(self, sched = schedule, file_name=None, overwrite=False):
        '''Given a schedule, write the contents of the schedule to a specific file as json data.'''
        # Get the correct file path, including .json extension
        if file_name == None:
            file_name = input("File name to write to? >> ")
        if not file_name.endswith('.json'): file_name += '.json'
        file_path = f'./schedules/{file_name}'
        
        try:
            if exists(file_path) and not overwrite: raise FileExistsError
            
            # Dump all the tasks in the schedule as correctly formatted json.
            with open(file_path, 'w') as f:
                json.dump(sched._tasks, f, indent=4, default=Task.Task.serialize)
        
        # Edge case for when the file already exists.
        # Notify user of already existing file, and ask if they want to override.
        except FileExistsError:
            print(f'File \'{file_path}\' already exists.')
            override = input('Would you like to overwrite it? [Y/N] >> ')
            while override != 'Y' and override != 'N':
                override = input('Would you like to overwrite it? [Y/N] >> ')
            if override == 'Y':
                self.write(file_name=file_name, overwrite=True)
            
        except Exception as e:
            print('Sorry, something went wrong.')
            print(f'{e.__class__.__name__}: {e}')
        
        else:
            print(f'Schedule written to \'{file_path}\' successfully!')

    
    def happenOnDay(self, task, date):
        '''Returns true if task occurs on date, returns false otherwise. Task can be transient, recurring, or anti'''
        if type(task) == Task.Recurring:
            if task.start_date > date:    #Start date happens after the day we want, return false
                return False
            elif task.start_date == date:   #Start day happens on desired day, return true
                return True
            elif task.start_date < date:    #Start day happens before desired day, iterate to see if it occurs on day
                current_day = task.start_date
                while current_day <= date:
                    if current_day == date:  #Event occurs on desired day, return true
                        return True
                    current_day = current_day.plus(task.frequency)  #Increment current day
                return False

        elif type(task) == Task.Transient:
            if task.date == date:
                return True

        elif type(task) == Task.Anti:
            if task.date == date:
                return True
            
    #NOTE: The write methods here will take all tasks that occur in the specified time and add them to the json file. Only one instance of a recurring task is added
    def write_day(self):
        date = Date(input("Enter the date: "))
        daySchedule = Schedule()    #Schedule to write to file
        for task in schedule._tasks:    #Iterate through all tasks...
            if(self.happenOnDay(task, date)):   #If task happens on this date...
                daySchedule._tasks.append(task) #Add it to the schedule...
        self.write(daySchedule) #Write the schedule to a file
    
    def write_week(self):
        '''Creates a schedule of all tasks that occur on the day entered, and all tasks that occur on the following seven days'''
        date = Date(input("Enter the date for the start of the week: "))
        weekSchedule = Schedule()   #Schedule to write to file
        alreadyAdded = []   #List of tasks already added to schedule
        for i in range(0, 7):   #Iterate through 7 days (1 week)
            for task in schedule._tasks:
                if self.happenOnDay(task, date):
                    if task.name not in alreadyAdded:   #If task has already been added then it is recursive, don't add it again
                        weekSchedule._tasks.append(task)
                        alreadyAdded.append(task.name)  #If we add the task to schedule, at it to list so we know not to add it again
            date = date.plus(1) #Go to the next day
        self.write(weekSchedule)
    
    def write_month(self):
        date = Date(input("Enter the date to start from (Days entered are irrelevant, but still enter the whole date): "))

        #Update the date to start at the beginning of the month, regaurdless as to what they entered
        date_list = list(date._date)
        date_list[6] = "0"  #Change last 2 digits of date to 0
        date_list[7] = "0"
        new_string = "".join(date_list)
        date._date = new_string
        date._day = "00"

        monthSchedule = Schedule()
        alreadyAdded = []
        for i in range(0, date._calendar[date._month]["days"]): #Check all days from start to end of month
            for task in schedule._tasks:
                if self.happenOnDay(task, date):
                    if task.name not in alreadyAdded:
                        monthSchedule._tasks.append(task)
                        alreadyAdded.append(task.name)
            date = date.plus(1)

        self.write(monthSchedule)



# -----------------------------------
file_handler = FileHandler() # This effectively acts as a singleton.