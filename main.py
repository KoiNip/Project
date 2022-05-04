from Schedule import schedule
import consolemenu as cm
import consolemenu.items as cmi

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
            "Read from file": schedule.read,
            "Write to file": {
                "one day": schedule.write_day,
                "one week": schedule.write_week,
                "one month": schedule.write_month,
                "entire schedule": schedule.write
            },
            "View": {
                "one day": schedule.view_day,
                "one week": schedule.view_week,
                "one month": schedule.view_month
            }
        }
    }

    gui=cm.ConsoleMenu("PSS", "CS 3560", clear_screen=False)
    buildMenu(gui, directory)
    gui.show()