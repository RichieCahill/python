"""DAY1_Part1"""

from pathlib import Path


class Game:
    """Game."""

    def __init__(self, input_data: list[str]) -> None:
        """Initialize the game."""
        self.faculty_map: list[list[str]] = []
        self.direction = "^"

        for index, line in enumerate(input_data):
            current_line = line
            if self.direction in line:
                self.x = index
                self.y = line.index(self.direction)
                current_line = current_line.replace(self.direction, ".")

            self.faculty_map.append(list(current_line))
            self.x_max = len(self.faculty_map[0])
            self.y_max = len(self.faculty_map)

    def move(self) -> bool:
        """Move the position."""
        if self.direction == "^":
            new_x = self.x - 1
            test = self.faculty_map[new_x][self.y]
            if new_x >= self.x_max:
                return True
            if test == "#":
                self.direction = ">"
                return False
            self.x = new_x
            return False

        if self.direction == ">":
            new_y = self.y + 1
            if new_y >= self.y_max:
                return True
            if self.faculty_map[self.x][new_y] == "#":
                self.direction = "v"
                return False
            self.y = new_y
            return False
        if self.direction == "v":
            new_x = self.x + 1
            if new_x >= self.x_max:
                return True
            if self.faculty_map[new_x][self.y] == "#":
                self.direction = "<"
                return False
            self.x = new_x
            return False
        if self.direction == "<":
            new_y = self.y - 1
            if new_y < 0:
                return True
            if self.faculty_map[self.x][new_y] == "#":
                self.direction = "^"
                return False
            self.y = new_y
            return False
        error = "Invalid direction"
        raise ValueError(error)

    def explore_faculty(self) -> None:
        """Explore the faculty."""
        starting_position: tuple[int, int] = (self.x, self.y)
        explored = set()
        current_position: tuple[int, int] = starting_position
        while True:
            if self.move():
                break
            explored.add(current_position)
            current_position = (self.x, self.y)

        explored_count = len(explored) + 1
        print(f"{explored_count=}")

    def display(self) -> None:
        """Display the faculty."""
        test = self.faculty_map
        test[self.x][self.y] = self.direction
        for line in test:
            print(line)


def main() -> None:
    """Main function to read input file and calculate the sum of numbers in each line."""
    input_file = Path("./advent_of_code/2024/day06.txt")
    input_data = input_file.read_text().splitlines()

    game = Game(input_data)

    game.explore_faculty()


if __name__ == "__main__":
    main()
