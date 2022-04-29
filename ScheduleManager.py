import Task

class ScheduleManager:
    _tasks = []
    
    def add(self, task):
        '''Adds a task to the ScheduleManager.'''
        if task.name in [t.name for t in self._tasks]: raise TypeError(f'A task with the name \'{task.name}\' already exists.')
        self._tasks.append(task)
    
    def view(self, name):
        '''Returns a task that exists in the ScheduleManager'''
        if name not in [t.name for t in self._tasks]: raise TypeError(f'No task exists with the name \'{name}\'')
        
        for index, t in enumerate(self._tasks):
            if t.name == name: break
        return self._tasks[index]

    def delete(self, name):
        if name not in [t.name for t in self._tasks]: raise TypeError(f'No task exists with the name \'{name}\'')

        for index, t in enumerate(self._tasks):
            if t.name == name: break
        self._tasks.remove(index)
    
    def edit(self, name, task):
        if name not in [t.name for t in self._tasks]: raise TypeError(f'No task exists with the name \'{name}\'')

        self.delete(name)
        self.add(task)
    
manager = ScheduleManager()