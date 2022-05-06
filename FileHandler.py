import json
import os
from os.path import exists
from Schedule import schedule
import Task

class FileHandler():
    def read(self):
        file_name = input("File name to read from? >> ")
        if not file_name.endswith('.json'): file_name += '.json'
        file_path = f'./schedules/{file_name}'
        
        try:
            if not exists(file_path): raise FileNotFoundError
            with open(file_path) as infile:
                schedule_as_json = json.load(infile)
            for task in schedule_as_json:
                print(task)
                try:
                    new_tasks = []
                    schedule._tasks = new_tasks
                except Exception as e:
                    print('Sorry, something went wrong.')
                    print(f'{e.__class__.__name__}: {e}')
                    
        except json.JSONDecodeError:
            print(f'File \'{file_path}\' contains invalid JSON or is corrupted.')
        except FileNotFoundError:
            print(f'File \'{file_path}\' does not exist.')
        else:
            print(f'Schedule loaded from \'{file_path}\' successfully!')
    
    def write(self, file_name=None, overwrite=False):
        if file_name == None:
            file_name = input("File name to write to? >> ")
        if not file_name.endswith('.json'): file_name += '.json'
        file_path = f'./schedules/{file_name}'
        
        try:
            if exists(file_path) and not overwrite: raise FileExistsError
            
            with open(file_path, 'w') as f:
                json.dump(schedule._tasks, f, indent=4, default=Task.Task.serialize)
        
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
            
    def write_day(self):
        pass
    
    def write_week(self):
        pass
    
    def write_month():
        pass

# -----------------------------------
file_handler = FileHandler()