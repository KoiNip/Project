from Schedule import schedule
from FileHandler import file_handler
import consolemenu as cm
import consolemenu.items as cmi
import Task
import sys

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
    directory = {
        "Tasks": {
            "Create": schedule.add_task,
            "View": schedule.view,
            "Delete": schedule.delete,
            "Edit": schedule.edit
        },
        "Schedule": {
            "Read from file": file_handler.read,
            "Write to file": {
                "one day": schedule.write_day,
                "one week": schedule.write_week,
                "one month": schedule.write_month,
                "entire schedule": file_handler.write
            },
            "View": {
                "one day": schedule.view_day,
                "one week": schedule.view_week,
                "one month": schedule.view_month
            }
        }
    }

    gui=cm.ConsoleMenu("PSS", "CS 3560", clear_screen=False, show_exit_option=True)
    buildMenu(gui, directory)
    
    test_recurring = Task.Recurring(
        name='catching some zzz',
        category='Sleep',
        start_time=22.5,
        duration=8,
        start_date=20220503,
        end_date=20221231,
        frequency=1
    )
    
    test_transient = Task.Transient(
        name = 'Go gym',
        category = 'Visit',
        start_time = 9.5,
        duration=2,
        date=20220509
    )
    
    test_anti = Task.Anti(
        name='I really didn\'t want to walk',
        category='Cancellation',
        date=20200415,
        start_time=10.25,
        duration=0.75
    )
    
    schedule._tasks.append(test_recurring)
    schedule._tasks.append(test_transient)
    schedule._tasks.append(test_anti)
    
    gui.show()