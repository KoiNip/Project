import sys
from Schedule import schedule
import Task

def doSomeFunction():
    print('function doSomeFunction() has ran')
    
class TextGuidedMenuSystem:
    def __init__(self, directory, decorator, indent, welcome_msg, main_msg):
        self.directory = directory
        self.decorator = decorator
        self.indent = indent
        self.welcome_msg = welcome_msg
        self.main_msg = main_msg
        
    def run(self):
        current_directory = self.directory
        level = 0
        
        print(f'{self.welcome_msg}\n{self.decorator*50}')
        while True:
            spacing = self.indent*level
            if level == 0: print(f'{self.main_msg}\n{self.decorator*len(self.main_msg)}')

            # Display options from current directory
            for idx, option in enumerate(current_directory):
                print(f'{spacing}{idx} {option}')
            print(f'q Exit') if level == 0 else print(f'{spacing}b Back')

            # Get selection from user
            selection = input(f'{spacing}> ')
            print()

            # Branch off based upon selection number
            if selection in [str(i) for i, _ in enumerate(current_directory)]:
                key = list(current_directory.keys())[int(selection)]
                print(f'{spacing}{key}\n{spacing}{self.decorator*len(key)}')

                # If the value of the selected key is a dictionary...
                if type(current_directory[key]) == dict:
                    current_directory = current_directory[key]
                    level += 1

                # If the value of the selected key is a function...
                elif callable(current_directory[key]):
                    current_directory[key]()
                    continue

                # If the value of the selected key is something else...
                else: raise AssertionError(f'This should never be executed.\nThe value associated with {key = } was neither a dictionary or function')

            elif selection == 'b' and level != 0:
                level -= 1
            elif selection == 'q' and level == 0:
                print('Thanks for using PSS, goodbye.')
                sys.exit(0)
            else:
                print(f'{spacing}Please select a valid option.')

def main():
    directory = {
        "Tasks": {
            "Create": doSomeFunction,
            "View": doSomeFunction,
            "Delete": doSomeFunction,
            "Edit": doSomeFunction
        },
        "Schedule": {
            "Read from file": doSomeFunction,
            "Write to file": {
                "one day": doSomeFunction,
                "one week": doSomeFunction,
                "one month": doSomeFunction,
                "entire schedule": doSomeFunction
            },
            "View": {
                "one day": doSomeFunction,
                "one week": doSomeFunction,
                "one month": doSomeFunction
            }
        }
    }
    
    main_menu = TextGuidedMenuSystem(
        directory=directory,
        decorator='-',
        indent='    ',
        welcome_msg='Welcome to PSS. What would you like to do?',
        main_msg='Main menu'
    )
    
    main_menu.run()

if __name__ == '__main__':
    main()