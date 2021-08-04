def my_function():
  print("Hello world")

my_function()

def my_function(test):
  print(test)

my_function("hello world")

def my_function(test1, test2):
  print(test1+" "+test2)

my_function("Hello", "world")

def my_function(*movie):
  print("The BEST Starwars movie " + movie[3])

my_function("Star Wars I", "Star Wars II", "Star Wars III", "Star Wars IV", "Star Wars V", "Star Wars VI") 

def my_function(x):
  return 5 * x

print(my_function(3))
print(my_function(5))
print(my_function(9))


def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))


def mydoubler2 (n):
  return 2 * n
def mytripler2 (n):
  return 3 * n

print(mydoubler2(11))
print(mytripler2(11))