"""DAY1_Part1"""

from pathlib import Path
import re


def multiply(string: str) -> int:
    """Multiply the numbers in the string."""
    left, right = string.removeprefix("mul(").removesuffix(")").split(",")
    return int(left) * int(right)


def main() -> None:
    """Main function to read input file and calculate the sum of numbers in each line."""
    input_file = Path("./advent_of_code/2024/day03.txt")
    input_data = input_file.read_text()

    processed_data = "    ".join(part.split("don't()")[0] for part in input_data.split("do()"))

    regex = re.compile(r"mul\([\d]{1,3},[\d]{1,3}\)")
    output = sum(multiply(instruction) for instruction in regex.findall(processed_data))

    print(output)


if __name__ == "__main__":
    main()
