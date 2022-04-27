from TaskManager import TaskManager
import sys

class Menu:
    def __init__(self):
        pass
    
    def quitFunc(self):
        print(f'Thanks for using PSS, goodbye.')
        sys.exit(0)
    
    directory = {
        'Tasks': {
            'Create a task': TaskManager.create,
            'View a task': TaskManager.view,
            'Delete a task': TaskManager.delete,
            'Edit a task': TaskManager.edit
        },
        'Schedule': {
            'Write the schedule to a file': Schedule.write,
            'Read the schedule from a file': Schedule.read,
            'View or write the schedule for one day': Schedule.view,
            'View or write the schedule for one week': Schedule.view,
            'View or write the schedule for one month': Schedule.view
        }
    }
    
    def display(self):
        while True:
            for i, t in enumerate(self.directory):
                print(f"    {i} {t}")
            print(f"    q Exit")
            x = input("> ")
            
            if x in [str(i) for i, _ in enumerate(self.directory)]:
                if isinstance(self.directory[list(self.directory)[int(x)]], dict):
                    print(f"    {list(self.directory)[int(x)]}")
                    for i2, t2 in enumerate(self.directory[list(self.directory)[int(x)]]):
                        print(f"        {i2} {t2}")
                    print(f"        b Back")
                    x2 = input("> ")
                    
                    if x2 in [str(i) for i, _ in enumerate(self.directory[list(self.directory)[int(x)]])]:
                        pass
                    elif x2 == 'b':
                        continue
                    else:
                        print("Please select an option, or go back")
                        
            elif x == 'q':
                self.quitFunc(self)
            else:
                print("Please select an option, or exit")
            print()