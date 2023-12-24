"""DAY7_Part1"""
from pathlib import Path


def clean_data(input_data: list[str]) -> list[list[int]]:
    """Clean data"""
    output_data = []
    for line in input_data:
        output_line = [int(char) for char in line.split(" ")]
        output_data.append(output_line)
    return output_data


def calculate_maps(input_data: list[list[int]]) -> list[list[int]]:
    """calculate_maps"""
    output_data = []
    max_iter = 100
    for item_1 in input_data:
        test = [item_1]
        count = 0
        while set(test[-1]) != {0}:
            temp = []
            for index, item in enumerate(test[-1]):
                if index + 1 == len(test[-1]):
                    break
                temp.append(test[-1][index + 1] - item)
            test.append(temp)

            count += 1
            if count >= max_iter:
                break
        test.sort(key=lambda x: len(x))
        output_data.append(test)

    return output_data


def get_history(change_map: list[int]) -> int:
    """get_history"""
    print(change_map)
    for index, row in enumerate(change_map):
        if index + 1 == len(change_map):
            return row[-1]
        thing = row[-1] + change_map[index + 1][-1]
        change_map[index + 1].append(thing)
    return 0


def main() -> None:
    input_file = Path("./Advent_of_code/2023/DAY9_Part1.txt")
    input_data = input_file.read_text().splitlines()

    input_data = clean_data(input_data)

    change_maps = calculate_maps(input_data)

    output = sum([get_history(change_map) for change_map in change_maps])

    print(output)


main()
