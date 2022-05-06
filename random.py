import json
import Task

file_path = './schedules/testing1.json'

new_tasks = []

task_types = {
    "Recurring": [
        'Class',
        'Study',
        'Sleep',
        'Exercise',
        'Work',
        'Meal'
    ],
    "Transient": [
        'Visit',
        'Shopping',
        'Appointment'
    ],
    "Anti": [
        'Cancellation'
    ]
}

all_possible_task_types = [item for sublist in task_types.values() for item in sublist]

def dict_as_recurring(dict):
    print('am i here1')
    for attribute in dict:
        print(attribute)
        if attribute not in dir(Task.Recurring):
            # raise json.JSONDecodeError("No JSON object could be decoded", dict, 0)
            raise ValueError
        
    return Task.Recurring(
        name=dict['name'],
        category=dict['type'],
        start_time=dict['start_time'],
        duration=dict['duration'],
        start_date=dict['start_date'],
        end_date=dict['end_date'],
        frequency=dict['frequency']
    )
    
def dict_as_transient(dict):
    print('am i here2')
    for attribute in dict:
        print(attribute)
        if attribute not in dir(Task.Transient):
            # raise json.JSONDecodeError("No JSON object could be decoded", dict, 0)
            raise ValueError
    
    return Task.Transient(
        name=dict['name'],
        category=dict['category'],
        start_time=dict['start_time'],
        duration=dict['duration'],
        date=dict['date']
    )
    
def dict_as_anti(dict):
    print('am i here3')
    for attribute in dict:
        print(attribute)
        if attribute not in dir(Task.Anti):
            # raise json.JSONDecodeError("No JSON object could be decoded", dict, 0)
            raise ValueError
        
    return Task.Anti(
        name=dict['name'],
        category=dict['category'],
        start_time=dict['start_time'],
        duration=dict['duration'],
        date=dict['date']
    )
    

with open(file_path) as infile:
    schedule_as_json = json.load(infile)

for obj in schedule_as_json:
    try:
        if obj['type'] not in all_possible_task_types:
            raise ValueError

        if obj['type'] in task_types['Recurring']:
            temp = json.loads(obj, object_hook=dict_as_recurring)

        elif obj['type'] in task_types['Transient']:
            temp = json.loads(obj, object_hook=dict_as_transient)

        elif obj['type'] in task_types['Anti']:
            temp = json.loads(obj, object_hook=dict_as_anti)
    
    except json.JSONDecodeError:
        print(f'File contains invalid JSON or is corrupted og.')
    except ValueError:
        print(f'File contains invalid JSON or is corrupted og2.')
    
    else:
        new_tasks.append(temp)
        
print(new_tasks)
    