from math import sqrt
import time

def PrimeChecker(number):
	if number == 2:
		return True
	if number < 2:
		return False

	primes = [2]
	for i in range(3, int(sqrt(number)) + 1, 2):
		for prime in primes:
			# if i % prime == 0:
			if i % prime: # i think this is way faster
				break
		# primes.append(i)
		primes.extend(list(i))
	for prime in primes:
		# if number % prime == 0:
		if not number % prime:
			return False
	return True

# print(PrimeChecker(1124526947))
# print(PrimeChecker(106859*72689))
# print(PrimeChecker(1000000016531*5))
# print(PrimeChecker(5000000082655))



# test = [2, 3, 5, 7, 11, 13, 17, 19, 
# 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
# 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
# 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
# 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
# 233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
# 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
# 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
# 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
# 467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
# 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
# 607, 613, 617, 619, 631, 641, 643, 647, 653, 659]

# test=[PrimeChecker(prime) for prime in test]

# print(test)
# time.sleep(0.5)
start_time = time.time()
print(PrimeChecker(1000000001))
print(time.time() - start_time)
