import re
from math import prod
from pathlib import Path
from pprint import pprint


def get_race_stats(input_data: list[str]) -> list[list[str]]:
    """get_race_stats"""
    race_stats = []

    for line in input_data:
        raw_line = line.split(":")[1].strip()
        while "  " in raw_line:
            raw_line = raw_line.replace("  ", " ")
        race_stats.append(raw_line.split(" "))

    return list(zip(*race_stats, strict=True))


def calculate_result(time: int, distance_record: int) -> int:
    """caculate_distance"""
    counter = 0
    for acceliration in range(1, time):
        distance = acceliration * (time - acceliration)
        if distance > distance_record:
            counter += 1

    return counter


def main() -> None:
    input_file = Path("./Advent_of_code/2023/DAY6_Part1.txt")
    input_data = input_file.read_text().splitlines()

    race_stats = get_race_stats(input_data=input_data)

    number_of_wins = [
        calculate_result(time=int(time), distance_record=int(distance_record)) for time, distance_record in race_stats
    ]
    print(prod(number_of_wins))


main()


# edited part 2 input my hand because it was easier than writing the code to do it
