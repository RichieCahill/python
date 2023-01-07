cars = ["Ford", "Volvo", "BMW"] 
x = cars[0]

print (len(cars))
print (cars[0])
print (x)

cars[0] = "Toyota"
cars.append("Honda")

print (cars[3])

print (len(cars))
print (cars[0])
print (x)

x = cars[0]
print (x)

print (cars[1])
cars.remove("Volvo") 
print (cars[1])

#append()	  Adds an element at the end of the list
#clear()	  Removes all the elements from the list
#copy()	    Returns a copy of the list
#count()	  Returns the number of elements with the specified value
#extend()	  Add the elements of a list (or any iterable), to the end of the current list
#index()	  Returns the index of the first element with the specified value
#insert()	  Adds an element at the specified position
#pop()	    Removes the element at the specified position
#remove()	  Removes the first item with the specified value
#reverse()	Reverses the order of the list
#sort()	    Sorts the list