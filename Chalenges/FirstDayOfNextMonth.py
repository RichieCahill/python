from datetime import datetime, timedelta

Now = datetime.now().date()

# Solution 1
# Run time 800ms
# Creator ahuston-0
def month_inc(month, year):
	return (month+1, year) if month < 12 else (1, year+1)
def get_first_of_next_month(date):
	month, year = month_inc(date.month, date.year)
	return date.replace(year=year, month=month, day=1)

print(get_first_of_next_month(Now))

# Solution 2
# Run time 1.5S
# Creator TheMadMaker2
def NextMonth(date):
	return (date.replace(day=28)+timedelta(days=4)).replace(day=1)

print(NextMonth(Now))
