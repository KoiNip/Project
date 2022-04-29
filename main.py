from ScheduleManager import manager
import Task

def main():
    study = Task.Recurring(
        name='cs3560 quiz coming up',
        category='Study',
        start_time=8.59, 
        duration=1.75,
        start_date=20200414,
        end_date='20200419',
        frequency=1
    )
    # print(study.start_time)
    # print(study.start_date.pretty())

    manager.add(study)
    print(manager.view('cs3560 quiz coming up').to_json())

if __name__ == '__main__':
    main()