from Schedule import schedule
from FileHandler import file_handler
import consolemenu as cm
import consolemenu.items as cmi

def buildMenu(menu, directory):
    '''Helper function to recursively create the menu's within the GUI based on the directory structure.'''
    for k, v in directory.items():
        if type(v) == dict:
            submenu = cm.ConsoleMenu(subtitle=k, clear_screen=False, exit_option_text='Return')
            buildMenu(submenu, v)

            menu.append_item(cmi.SubmenuItem(k, submenu, menu))
        elif callable(v):
            menu.append_item(cmi.FunctionItem(k, v))
        else: raise AssertionError(f'This should never be executed.\nThe value associated with {k} was neither a dictionary or function')

if __name__ == '__main__':
    # Define the directory structure for the GUI  
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
                "one day": file_handler.write_day,
                "one week": file_handler.write_week,
                "one month": file_handler.write_month,
                "entire schedule": file_handler.write
            },
            "View": {
                "one day": schedule.view_day,
                "one week": schedule.view_week,
                "one month": schedule.view_month
            }
        }
    }

    # Create the GUI
    gui=cm.ConsoleMenu("PSS", "CS 3560", clear_screen=False, show_exit_option=True)
    buildMenu(gui, directory)
    
    # Display the GUI
    gui.show()