"""DAY1_Part1"""

from pathlib import Path


def main() -> None:
    """Main function to read input file and calculate the sum of numbers in each line."""
    input_file = Path("./advent_of_code/2024/day01.txt")
    input_data = input_file.read_text().splitlines()

    left_numbers = []
    right_numbers = []
    for line in input_data:
        left, right = line.split()
        left_numbers.append(int(left))
        right_numbers.append(int(right))

    left_numbers.sort()
    right_numbers.sort()

    total = sum(number * right_numbers.count(number) for number in left_numbers)

    print(total)


if __name__ == "__main__":
    main()
