from json import JSONEncoder

class Date():
    _calendar = {
    	'01': {'month': 'January', 'days': 31},
        '02': {'month': 'February', 'days': 28},
        '03': {'month': 'March', 'days': 31},
        '04': {'month': 'April', 'days': 30},
        '05': {'month': 'May', 'days': 31},
        '06': {'month': 'June', 'days': 30},
        '07': {'month': 'July', 'days': 31},
        '08': {'month': 'August', 'days': 31},
        '09': {'month': 'September', 'days': 30},
        '10': {'month': 'October', 'days': 31},
        '11': {'month': 'November', 'days': 30},
        '12': {'month': 'December', 'days': 31},
    }
    
    # Initialization
    def __init__(self, date):
        self._date = str(date)
        self._year = self._date[:4]
        self._month = self._date[4:6]
        self._day = self._date[6:8]
        
        # Parameter validation
        if not self._date.isdigit(): raise AssertionError('dates can only contain digits')
        if not len(self._date) == 8: raise AssertionError('dates must have a length of 8')
        if self._month not in self._calendar: raise AssertionError(f'month \'{self._month}\' is not defined (months must be 01 through 12)')
        if int(self._day) > self._calendar[self._month]['days']: raise AssertionError(f'date \'{self._date}\' does not exist, {self._calendar[self._month]["month"]} only has {self._calendar[self._month]["days"]} days')
    
    # Represenations
    def __str__(self):
        return self._date
    
    def __repr__(self):
        return self._date
        # return f'{self.__class__.__name__}({self._date})'
    
    def pretty(self):
        """Return a pretty version of the date as a string.
        >>> Date('20220427').pretty()
        'April 27, 2022'
        """
        return f'{self._calendar[self._month]["month"]} {self._day}, {self._year}'
        
    # Comparisons
    def __eq__(self, other): return self._date == other._date
    
    def __lt__(self, other): return self._date < other._date
    def before(self, other):
        """Return True if self occurs before other, False otherwise.
        >>> Date('20220427').before(Date('20220516'))
        True
        """
        return self._date < other._date
    
    def __gt__(self, other): return self._date > other._date
    def after(self, other): 
        """Return True if self occurs after other, False otherwise.
        >>> Date('20220427').after(Date('20220425'))
        True
        """
        return self._date > other._date
    
    def as_int(self):
        return int(self._date)
    
if __name__ == '__main__':
    today = Date('20220427')
    yesterday = Date(20220426)
    print(f'{today = }, also known as {today.pretty()}')
    print(f'{yesterday = }, also known as {yesterday.pretty()}')
    print(f'{today > yesterday = }')
    print(f'{today.before(yesterday) = }')
    print(f'{today.after(yesterday) = }')
    print()
    some_other_day = Date(20231040)