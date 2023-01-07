from random import randrange
from time import sleep
avr = [1, 2, 3]
ravr = [1, 2, 3]

def Avg(inp):
  avr.insert(0, inp)
  return(round(sum(avr) / len(avr)))

def RAvg(inp):
  ravr.insert(0, inp)
  if len(ravr) > 11:
    ravr.pop()
  return(round(sum(ravr) / len(ravr)))

while True:
  inp = randrange(1, 1000)
  print(inp)
  print(Avg(inp))
  print(RAvg(inp))
  sleep(0.5)
