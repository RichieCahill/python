"""DAY05_Part1"""

from pathlib import Path
from pprint import pprint


class Farm:
    """Farm"""

    def __init__(self, input_data: int) -> None:
        """Init"""
        data_dict = self._get_maps_and_seeds(input_data)
        self.seeds = data_dict["seeds"]
        self.soil_map = data_dict["seed-to-soil map:"]
        self.fertilizer_map = data_dict["soil-to-fertilizer map:"]
        self.water_map = data_dict["fertilizer-to-water map:"]
        self.light_map = data_dict["water-to-light map:"]
        self.temperature_map = data_dict["light-to-temperature map:"]
        self.humidity_map = data_dict["temperature-to-humidity map:"]
        self.location_map = data_dict["humidity-to-location map:"]

    def __repr__(self) -> str:
        """Repr"""
        return (
            f"seeds={self.seeds},\n"
            f"soil_map={self.soil_map},\n"
            f"fertilizer_map={self.fertilizer_map},\n"
            f"water_map={self.water_map},\n"
            f"light_map={self.light_map},\n"
            f"temperature_map={self.temperature_map},\n"
            f"humidity_map={self.humidity_map},\n"
            f"location_map={self.location_map}\n"
        )

    def _generate_tuple(self, item: str) -> tuple[int]:
        """Generate tuple"""
        return tuple(int(number) for number in item.split(" "))

    def _get_maps_and_seeds(self, input_data: str) -> dict[str, tuple[tuple[int, int, int]]]:
        """Get maps"""
        input_list = input_data.split("\n\n")
        seeds_data = input_list.pop(0)

        seeds_string = seeds_data.split(": ")[1]
        seeds = self._generate_tuple(seeds_string)

        output_dict = {"seeds": seeds}
        for section in input_list:
            lines = section.split("\n")
            name = lines.pop(0)
            output_dict[name] = tuple(self._generate_tuple(item) for item in lines)

        return output_dict

    def _map_number(self, number: int, map_list: list[tuple[int, int, int]]) -> int:
        """Map number"""
        for destination_start, source_start, length in map_list:
            temp = source_start + length
            if source_start <= number < temp:
                return destination_start + (number - source_start)
        return number

    def _get_location(self, seed: int) -> int:
        """Get location"""
        soil = self._map_number(seed, self.soil_map)
        fertilizer = self._map_number(soil, self.fertilizer_map)
        water = self._map_number(fertilizer, self.water_map)
        light = self._map_number(water, self.light_map)
        temperature = self._map_number(light, self.temperature_map)
        humidity = self._map_number(temperature, self.humidity_map)
        return self._map_number(humidity, self.location_map)

    def get_lowest_location(self) -> int:
        """Get lowest location"""
        locations = []
        for seed in self.seeds:
            location = self._get_location(seed)
            locations.append(location)
        return min(locations)


def main() -> None:
    """Main"""
    input_file = Path("./Advent_of_code/2023/DAY5_Part1.txt")
    input_data = input_file.read_text()
    farm = Farm(input_data)
    pprint(farm.get_lowest_location())


main()
