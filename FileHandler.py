from calendar import week
import json
import os
from os.path import exists
from Schedule import Schedule, schedule
import Task
from Date import Date
class FileHandler():
    def read(self):
        file_name = input("File name to read from? >> ")
        if not file_name.endswith('.json'): file_name += '.json'
        file_path = f'./schedules/{file_name}'
        
        try:
            if not exists(file_path): raise FileNotFoundError
            with open(file_path) as infile:
                schedule_as_json = json.load(infile)
            
            new_schedule = []
            
            task_types = {
                "Recurring": ['Class', 'Study', 'Sleep', 'Exercise', 'Work', 'Meal'],
                "Transient": ['Visit', 'Shopping', 'Appointment'],
                "Anti": ['Cancellation']
            }
            all_possible_task_types = [item for sublist in task_types.values() for item in sublist]
            generic_task_attributes = ['name', 'type', 'start_time', 'duration']
            
            def dict_to_recurring(dct):
                recurring_task_attributes = ['start_date', 'end_date', 'frequency']
                recurring_task_attributes.extend(generic_task_attributes)
                for attribute in dct:
                    if attribute not in recurring_task_attributes: raise AttributeError

                return Task.Recurring(
                    dct['name'], dct['type'], 
                    dct['start_time'], dct['duration'], 
                    dct['start_date'], dct['end_date'], 
                    dct['frequency'])
    
            def dict_to_transient(dct):
                transient_task_attributes = ['date']
                transient_task_attributes.extend(generic_task_attributes)
                for attribute in dct:
                    if attribute not in transient_task_attributes: raise AttributeError
                
                return Task.Transient(
                    dct['name'], dct['type'], 
                    dct['start_time'], dct['duration'], 
                    dct['date'])
                
            def dict_to_anti(dct):
                anti_task_attributes = ['date']
                anti_task_attributes.extend(generic_task_attributes)
                for attribute in dct:
                    if attribute not in anti_task_attributes: raise AttributeError
                    
                return Task.Anti(
                    dct['name'], dct['type'],
                    dct['start_time'], dct['duration'],
                    dct['date']
                )
            
            for dct in schedule_as_json:
                try:
                    if dct['type'] not in all_possible_task_types: raise AttributeError
                    
                    if dct['type'] in task_types['Recurring']: 
                        new_schedule.append(dict_to_recurring(dct))
                    elif dct['type'] in task_types['Transient']:
                        new_schedule.append(dict_to_transient(dct))
                    elif dct['type'] in task_types['Anti']:
                        new_schedule.append(dict_to_anti(dct))
                
                except AttributeError:
                    print(f'AttributeError: dict type could not be converted into a Recurring, Transient, or Anti Task.')
                    print(f'{dct = }')
                    
        except json.JSONDecodeError:
            print(f'File \'{file_path}\' contains invalid JSON or is corrupted.')
        except FileNotFoundError:
            print(f'File \'{file_path}\' does not exist.')
        else:
            schedule._tasks = new_schedule
            print(f'Schedule loaded from \'{file_path}\' successfully!')
    
    def write(self, sched = schedule, file_name=None, overwrite=False):
        if file_name == None:
            file_name = input("File name to write to? >> ")
        if not file_name.endswith('.json'): file_name += '.json'
        file_path = f'./schedules/{file_name}'
        
        try:
            if exists(file_path) and not overwrite: raise FileExistsError
            
            with open(file_path, 'w') as f:
                json.dump(sched._tasks, f, indent=4, default=Task.Task.serialize)
        
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
            
    def write_day(self, date):
        daySchedule = Schedule()
        allDayTask = Task.Transient("ALL_DAY", Task.Transient.task_types[0], 0, 23.75, date)
        for task in schedule._tasks:
            if task.overlaps(allDayTask):
                if type(task) == Task.Recurring:
                    temp = Task.Recurring(task.name, task.type, task.start_time, task.duration, date, date, 1)
                    daySchedule._tasks.append(temp)
                else:
                    daySchedule._tasks.append(task)
        self.write(daySchedule)
    
    def write_week(self, date):
        weekSchedule = Schedule()
        longTask = Task.Recurring("ALL_WEEK", Task.Recurring.task_types[0], 0, 23.75, date, date.plus(7), 1)
        for task in schedule._tasks:
            if task.overlaps(longTask):
                if type(task) != Task.Recurring:
                    weekSchedule._tasks.append(task)
                else:
                    recurTask = Task.Recurring(task.name, task.type, task.start_time, task.duration, date, date.plus(7), task.frequency)
                    weekSchedule._tasks.append(recurTask)
        self.write(weekSchedule)
    
    def write_month(self, month, year):
        monthSchedule = Schedule()
        start = Date(year + month + "01")
        end = Date(year + month + Date._calendar[month]['days'])
        longTask = Task.Recurring("ALL_MONTH", Task.Recurring.task_types[0], 0, 23.75, 1)
        for task in schedule._tasks:
            if task.overlaps(longTask):
                if type(task) != Task.Recurring:
                    monthSchedule._tasks.append(task)
                else:
                    recurTask = Task.Recurring(task.name, task.type, task.start_time, task.duration, start, end, task.frequency)
                    monthSchedule._tasks.append(recurTask)
        self.write(week)

# -----------------------------------
file_handler = FileHandler()