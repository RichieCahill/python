from pathlib import Path


def make_int_set(numbers: str) -> set[int]:
    numbers_clean = numbers.strip().replace("  ", " ")
    numbers_strip = numbers_clean.split(" ")
    return {int(i) for i in numbers_strip}


def main() -> None:
    """Main"""
    input_file = Path("./Advent_of_code/2023/DAY4_Part1.txt")
    input_data = input_file.read_text().splitlines()

    total = 0
    for line in input_data:
        card_numbers, winning_numbers = line.split(": ")[1].split(" | ")

        list_winning_numbers = make_int_set(card_numbers)
        list_card_numbers = make_int_set(winning_numbers)
        wining_value_count = len(list_card_numbers.intersection(list_winning_numbers))

        if wining_value_count == 0:
            continue
        total += 1 << (wining_value_count - 1)

    print(total)


main()
