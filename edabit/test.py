def combinations(*items):
  y=1
  for x in items:
    if x > 0:
      y=x*y
  return(y)
combinations(3, 7, 4)
combinations(2)
combinations(2, 3)
