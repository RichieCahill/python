"""DAY2_Part2"""
from math import prod
from pathlib import Path


def game_posable(results: str) -> bool:
    """Determines if the game is posable based on the results.

    Args:
        results (str): The results of the game.

    Returns:
        bool: True if the game is posable, False otherwise.
    """
    largest_count = {"red": 0, "green": 0, "blue": 0}

    results_groups = results.strip().split("; ")
    for results_group in results_groups:
        color_count = {}

        for value_color in results_group.split(", "):
            value, color = value_color.split(" ")
            color_count[color] = int(value)

        for color in ["red", "green", "blue"]:
            if color_count.get(color, 0) > largest_count[color]:
                largest_count[color] = color_count.get(color, 0)

    return prod(largest_count.values())


def main() -> None:
    """Main"""
    input_file = Path("./Advent_of_code/2023/DAY2_Part2.txt")
    input_data = input_file.read_text().splitlines()

    result = [game_posable(line.split(": ")[1]) for line in input_data]

    print(sum(result))


main()
