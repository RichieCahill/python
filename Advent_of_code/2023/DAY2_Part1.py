from pathlib import Path


def game_posable(results: str) -> bool:
    """
    Check if the given results are posable in the game.

    Args:
        results (str): The results of the game in the format "value color, value color, ..."

    Returns:
        bool: True if the results are posable, False otherwise.
    """
    cubes_total = {"red": 12, "green": 13, "blue": 14}

    results_groups = results.split("; ")
    for results_group in results_groups:
        color_count = {}
        for value_color in results_group.split(", "):
            value, color = value_color.split(" ")
            color_count[color] = int(value)
        for color in ["red", "green", "blue"]:
            if color_count.get(color, 0) > cubes_total[color]:
                return False

    return True


def main():
    input_file = Path("./Advent_of_code/2023/DAY2_Part1.txt")
    with input_file.open("r") as file:
        input_data = [line.strip() for line in file]

    result = 0
    for line in input_data:
        game, results = line.split(": ")
        if game_posable(results):
            result += int(game.replace("Game ", ""))

    print(result)


main()
