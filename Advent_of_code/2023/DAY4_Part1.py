import re
from math import prod
from pathlib import Path
from pprint import pprint


def make_int_set(numbers: str) -> set[int]:
    numbers_clean = numbers.strip().replace("  ", " ")
    numbers_strip = numbers_clean.split(" ")
    return {int(i) for i in numbers_strip}


def main():
    input_file = Path(
        "./Advent_of_code/2023/DAY4_Part1.txt"
    )
    with input_file.open("r") as file:
        input_data = [line.strip() for line in file]
    total = 0
    for line in input_data:
        card_numbers, winning_numbers = line.split(": ")[1].split(" | ")

        list_winning_numbers = make_int_set(card_numbers)
        list_card_numbers = make_int_set(winning_numbers)
        wining_value_count = len(list_card_numbers.intersection(list_winning_numbers))

        total += int(min(wining_value_count, 1) * (2 ** (wining_value_count - 1)))

    print(total)


main()
