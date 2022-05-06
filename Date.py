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
    def __eq__(self, other): 
        return self._date == other._date
    
    def __lt__(self, other): 
        return self._date < other._date
    
    def __gt__(self, other):
         return self._date > other._date
    
    # Helper functions
    def serialize(self):
        """Helper function for JSON serialization"""
        return int(self._date)
    
    def plus(self, days):
        """Helper function to add a certain amount of days to a current date.
        Returns a string.
        >>> Date(20220427).plus(7)
        '20220504'
        >>> Date(20220405).plus(13)
        '20220418'
        >>> Date(20221229).plus(8)
        '20230106'
        >>> Date(20150815).plus(50)
        '20151004'
        >>> Date(20250420).plus(366)
        '20260421'
        """
        max_days_in_current_month = self._calendar[self._month]['days']
        
        new_year = int(self._year)
        new_month = int(self._month)
        new_day = int(self._day) + days
        
        while(int(new_day) > max_days_in_current_month):
            new_day = int(new_day)
            new_day -= max_days_in_current_month
            if (int(new_month) + 1 <= 12):
                new_month = int(new_month) + 1
            else:
                new_month = int(new_month) - 11
                new_year += 1
            
            if new_day < 10: new_day = '0' + str(new_day)
            if new_month < 10: new_month = '0' + str(new_month)
            max_days_in_current_month = self._calendar[str(new_month)]['days']
            
        if (int(new_month) < 10) and (len(str(new_month)) == 1): new_month = '0' + str(new_month)
            
        return f'{new_year}{new_month}{new_day}'

if __name__ == '__main__':
    # today = Date('20220427')
    # yesterday = Date(20220426)
    # print(f'{today = }, also known as {today.pretty()}')
    # print(f'{yesterday = }, also known as {yesterday.pretty()}')
    # print(f'{today > yesterday = }')
    # print()
    # print(f'{today + yesterday = }')
    # some_other_day = Date(20231040)
    print(f'[{"T" if Date(20220427).plus(7)=="20220504" else "F"}] {Date(20220427).plus(7) = }, should be 20220504')
    print(f'[{"T" if Date(20220405).plus(13)=="20220418" else "F"}] {Date(20220405).plus(13) = }, should be 20220418')
    print(f'[{"T" if Date(20221229).plus(8)=="20230106" else "F"}] {Date(20221229).plus(8) = }, should be 20230106')
    print(f'[{"T" if Date(20150815).plus(50)=="20151004" else "F"}] {Date(20150815).plus(50) = }, should be 20151004')
    print(f'[{"T" if Date(20250420).plus(366)=="20260421" else "F"}] {Date(20250420).plus(366) = }, should be 20260421')