from Schedule import schedule
import Task
import consolemenu as cm
import consolemenu.items as cmi

def doSomeFunction():
    print('doSomeFunction() executed...')

def buildMenu(menu, directory):
    for k, v in directory.items():
        if type(v) == dict:
            submenu = cm.ConsoleMenu(subtitle=k, clear_screen=False, exit_option_text='Return')
            buildMenu(submenu, v)

            menu.append_item(cmi.SubmenuItem(k, submenu, menu))
        elif callable(v):
            menu.append_item(cmi.FunctionItem(k, v))
        else: raise AssertionError(f'This should never be executed.\nThe value associated with {k} was neither a dictionary or function')

if __name__ == '__main__':
    first_task = Task.Transient(
        name='grocery shopping', 
        category='Shopping', 
        start_time=10.5, 
        duration=2, 
        date=20220514
    )
    
    directory = {
        "Tasks": {
            "Create": schedule.add_task,
            "View": first_task.view,
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
    
    # schedule.add(first_task)
    
    menu=cm.ConsoleMenu("PSS", "CS 3560", clear_screen=False)
    buildMenu(menu, directory)
    menu.show()