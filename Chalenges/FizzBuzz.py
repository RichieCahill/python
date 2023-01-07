# This loops from 1 to n printing output or num if output is empty
def fizzBuzz(n):
	for number in range(1,n):
		output = ""
		if number % 3 == 0:
			output ="".join((output,"Fizz "))
		if number % 5 == 0:
			output ="".join((output,"Buzz "))

		if output == "": 
			print(number)
			continue
		print(output)

fizzBuzz(25)