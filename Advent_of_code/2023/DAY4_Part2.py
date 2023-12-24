import re
from math import prod
from pathlib import Path
from pprint import pprint


def make_int_set(numbers: str) -> set[int]:
    """
    Converts a string of numbers into a set of integers.

    Args:
        numbers (str): A string of numbers separated by spaces.

    Returns:
        set[int]: A set containing the converted integers.
    """
    numbers_clean = numbers.strip().replace("  ", " ")
    numbers_strip = numbers_clean.split(" ")
    return {int(i) for i in numbers_strip}


def add_to_list_of_copy_of_tickets(
    list_of_copy_of_tickets: list[int],
    index: int,
    wining_value_count: int,
    copy_of_tickets: int,
) -> list[int]:
    """
    Adds the specified number of copies of tickets to the list of copy of tickets.

    Args:
        list_of_copy_of_tickets (list[int]): The list of copy of tickets.
        index (int): The starting index to add the copies of tickets.
        wining_value_count (int): The number of winning values.
        copy_of_tickets (int): The number of copies of tickets to add.

    Returns:
        list[int]: The updated list of copy of tickets.
    """
    for _ in range(copy_of_tickets):
        for ticket_number in range(wining_value_count):
            list_of_copy_of_tickets[ticket_number + index] += 1
    return list_of_copy_of_tickets


def count_winning_tickets(
    card_numbers: list[int],
    winning_numbers: list[int],
) -> int:
    """
    Counts the number of winning tickets by finding the intersection of card_numbers and winning_numbers.

    Args:
        card_numbers (list[int]): List of card numbers.
        winning_numbers (list[int]): List of winning numbers.

    Returns:
        int: Number of winning tickets.
    """
    list_winning_numbers = make_int_set(card_numbers)
    list_card_numbers = make_int_set(winning_numbers)
    return len(list_card_numbers.intersection(list_winning_numbers))


def main():
    """
    This function reads input data from a file, processes it, and prints the sum of a list of tickets.

    Returns:
        None
    """
    input_file = Path("./Advent_of_code/2023/DAY4_Part2.txt")
    input_data = input_file.read_text().splitlines()

    list_of_copy_of_tickets = [1] * len(input_data)
    list_of_copy_of_tickets[1] = 1
    for index, line in enumerate(input_data, 1):
        card_numbers, winning_numbers = line.split(": ")[1].split(" | ")

        wining_value_count = count_winning_tickets(
            card_numbers=card_numbers,
            winning_numbers=winning_numbers,
        )

        list_of_copy_of_tickets = add_to_list_of_copy_of_tickets(
            list_of_copy_of_tickets=list_of_copy_of_tickets,
            index=index,
            wining_value_count=wining_value_count,
            copy_of_tickets=list_of_copy_of_tickets[index - 1],
        )

    print(sum(list_of_copy_of_tickets))


main()
