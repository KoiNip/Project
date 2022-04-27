from TaskManager import manager
import Task

def main():
    # m = menu.Menu
    # m.display(m)
    
    study = Task.Recurring(
        name='study', 
        start_time=8.59, 
        duration=1.75,
        start_date=20200414,
        end_date=20200419,
        frequency=1
    )
    print(study)

if __name__ == '__main__':
    main()