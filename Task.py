from dataclasses import dataclass

@dataclass
class Task:
    name: str
    start_time: float
    duration: float
    
    # def __init__(self, name, start_time, duration):
    #     self.name = name
    #     self.start_time = start_time
    #     self.duration = duration
    
    def validate_input(self):
        if not (0 <= self.start_time <= 23.75):
            raise TypeError(f"start_time must be a positive number from 0 (midnight) to 23.75 (11:45 pm)")
        self.start_time = round(self.start_time, 0.25)
        
        if not (0.25 <= self.duration <= 23.75):
            raise TypeError(f"duration must be a positive number from 0.25 to 23.75")
        self.duration = round(self.duration, 0.25)
        
    validate_input()
    
@dataclass
class Recurring(Task):
    start_date: int
    end_date: int
    frequency: int

@dataclass
class Transient(Task):
    date: int

@dataclass
class Anti(Task):
    date: int