#https://edabit.com/challenge/2zKetgAJp4WRFXiDT
# how dos i and return work
def number_length(num):
  str = str(num)
  counter = 0    
  for i in str:
      counter += 1
  return counter

print(number_length(str))

def number_length(num):
  return sum(1 for i in str(num))