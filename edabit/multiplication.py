def list_of_multiples (num, length):  
  thislist = []
  i = 1
  while i <= length:    
    thislist.append(num*i)
    i += 1
  return thislist


list_of_multiples(7, 5)
