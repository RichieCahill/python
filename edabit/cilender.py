def weight(r, h):
  from math import pi
  #get the volume of the cylinder in cm
  cm = pi*r**2*h
  #Converst to dm and rounds to the second decimal place
  return round(cm/1000, 2)

weight(30, 60)
