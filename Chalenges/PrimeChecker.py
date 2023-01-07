from math import sqrt

def PrimeChecker(number):
    if number == 2:
        return True
    if number < 2:
        return False

    primes = [2]

    for i in range(3, int(sqrt(number)) + 1, 2):
        is_prime = True
        for prime in primes:
            if i % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    for prime in primes:
        if number % prime == 0:
            return False
    return True

print(PrimeChecker(1000000001))


