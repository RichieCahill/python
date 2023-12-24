"""DAY7_Part1"""
from pathlib import Path
from pprint import pprint


z


def calculate_distance_between_galaxies(universe: Universe) -> dict:
    """calculate_distance_between_galaxies"""
    distances = []
    for index, galaxy in enumerate(universe.galaxies):
        distances.extend(
            [
                universe.get_distance(galaxy, other_galaxy)
                for other_galaxy in universe.galaxies[index + 1 :]
            ]
        )
    return distances


def main():
    input_file = Path("./Advent_of_code/2023/DAY11_Part2.txt")
    with input_file.open("r") as file:
        input_data = [line.strip() for line in file]

    universe = Universe(input_data=input_data)

    distances = calculate_distance_between_galaxies(universe=universe)
    pprint(sum(distances))


main()
