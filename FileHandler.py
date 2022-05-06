import json
import os
from os.path import exists
from Schedule import schedule
import Task

class FileHandler():
    def read():
        pass
    
    def write(self, file_name=None, overwrite=False):
        if file_name == None:
            file_name = input("File name to write to? >> ")
        
        file_path = f'./schedules/{file_name}.json'
        
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