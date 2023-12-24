from random import randint


def test1(number: int) -> int:
    if number == 0:
        return 0
    if number == 1:
        return 1
    return int(2 ** (number - 1))


def test2(number: int) -> int:
    return min(number, 1) * int(2 ** (number - 1))


def test3(number: int) -> int:
    if number == 0:
        return 0
    return int(2 ** (number - 1))


def test4(number: int) -> int:
    if number == 0:
        return 0
    return int(1 << (number - 1))


def test5(number: int) -> int:
    if number == 0:
        return 0
    return 1 << (number - 1)


def test6(number: int) -> int:
    return min(number, 1) << (max(number - 1, 0))


def main() -> None:
    # number_of_tests = 1_000_000_000
    number_of_tests = 1_000_000

    test1_results = 0
    test2_results = 0
    test3_results = 0
    test4_results = 0
    test5_results = 0
    test6_results = 0

    for _ in range(number_of_tests):
        random_number = randint(0, 100)
        test5_results += test5(random_number)
        test4_results += test4(random_number)
        test3_results += test3(random_number)
        test2_results += test2(random_number)
        test1_results += test1(random_number)
        test6_results += test6(random_number)

    print(test1_results)
    print(test2_results)
    print(test3_results)
    print(test4_results)
    print(test5_results)
    print(test6_results)


if __name__ == "__main__":
    main()


"""results

15m:51.543s
1_000_000_000
randint(0, 100)

        │Time    │–––––– │–––––– │
  Line  │Python  │native │system │/home/r2r0m0c0/Projects/Python/prefoment_test.py
      3 │   13%  │       │       │test1
     11 │   18%  │       │       │test2
     15 │   14%  │       │       │test3
     21 │   11%  │       │       │test4
     27 │    6%  │       │       │test5
     33 │   15%  │       │       │test6
     37 │   20%  │       │       │main

15m:19.537s
1_000_000_000
randint(1, 100)
        │Time    │–––––– │–––––– │
  Line  │Python  │native │system │/home/r2r0m0c0/Projects/Python/prefoment_test.py
      3 │   13%  │       │       │test1
     11 │   19%  │       │       │test2
     15 │   14%  │       │       │test3
     21 │   11%  │       │       │test4
     27 │    5%  │       │       │test5
     33 │   15%  │       │       │test6
     37 │   20%  │       │       │main

397.983ms
1_000_000
randint(0, 100)
        │Time    │–––––– │–––––– │
  Line  │Python  │native │system │/home/r2r0m0c0/Projects/Python/prefoment_test.py
      3 │   31%  │    7% │   1%  │test1
     27 │   11%  │       │       │test5
     37 │   46%  │    2% │   1%  │main

414.519ms
1_000_000
randint(1, 100)
        │Time    │–––––– │–––––– │
  Line  │Python  │native │system │/home/r2r0m0c0/Projects/Python/prefoment_test.py
      3 │   27%  │       │       │test1
     27 │   13%  │       │       │test5
     37 │   46%  │   10% │   3%  │main
"""
