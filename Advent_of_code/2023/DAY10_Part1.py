"""DAY7_Part1"""
from pathlib import Path


class Position:
    """Position"""

    def __init__(self, x: int, y: int) -> None:
        """Init"""
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Repr"""
        return f"Position(x={self.x}, y={self.y})"

    def __add__(self, other: "Position") -> "Position":
        """Add"""
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other: "Position") -> bool:
        """Eq"""
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Hash"""
        return hash((self.x, self.y))


def make_grid(input_data: list[str]) -> list[list[str]]:
    """Make_grid"""
    return [list(row) for row in input_data]


def find_start_position(input_data: list[str]) -> Position:
    """Find_start_position"""
    for row in input_data:
        if "S" in row:
            return Position(row.index("S"), input_data.index(row))
    error = "No starting position found."
    raise ValueError(error)


def get_connected_pipes(current_position: Position, grid: list[list[str]]) -> list[Position]:
    """get_connected_pipes"""
    right = Position(1, 0)
    left = Position(-1, 0)
    down = Position(0, 1)
    up = Position(0, -1)
    connections = {
        "|": [up, down],
        "-": [left, right],
        "L": [up, right],
        "J": [up, left],
        "7": [down, left],
        "F": [down, right],
        "S": [up, down, left, right],
    }

    tile = grid[current_position.y][current_position.x]
    return [current_position + offset for offset in connections.get(tile, [])]


def is_valid(position: Position, grid_size: tuple[int, int]) -> bool:
    """Checks if the coordinates (x, y) are within the bounds of the grid."""
    return 0 <= position.x < grid_size[0] and 0 <= position.y < grid_size[1]


def trace_loop(start: Position, grid: list[list[str]]) -> dict[tuple[int, int], int]:
    """Traces the loop from the starting position and calculates the distance of each tile from the start."""
    distance_map = {}
    queue: list[tuple[Position, int]] = [(start, 0)]
    grid_size = (len(grid[0]), len(grid))

    while queue:
        position, dist = queue.pop(0)
        if position in distance_map:
            continue

        distance_map[position] = dist

        queue.extend(
            [
                (new_position, dist + 1)
                for new_position in get_connected_pipes(position=position, grid=grid)
                if is_valid(position=new_position, grid_size=grid_size) and new_position not in distance_map
            ],
        )

    return distance_map


def main() -> None:
    """Main"""
    input_file = Path("./Advent_of_code/2023/DAY10_Part1.txt")
    input_data = input_file.read_text().splitlines()

    start_position = find_start_position(input_data)
    grid = make_grid(input_data)

    distance_map = trace_loop(start_position, grid)
    print(distance_map)
    print(max(distance_map.values()))


main()
