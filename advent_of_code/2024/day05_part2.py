"""DAY1_Part1"""

from collections import defaultdict
from pathlib import Path


def check_pages(raw_pages: str, before_rules: dict[int, set[int]], after_rules: dict[int, set[int]]) -> bool:
    """Check the pages."""
    pages = [int(page) for page in raw_pages.split(",")]
    for index, page in enumerate(pages):
        pages_after_page = set(pages[index + 1 :])
        valid_before_rules = before_rules[page].intersection(pages_after_page)
        if len(valid_before_rules) != 0 and pages_after_page.difference(valid_before_rules) != set():
            return False

        pages_before_page = set(pages[:index])
        valid_after_rules = after_rules[page].intersection(pages_before_page)
        if len(valid_after_rules) != 0 and pages_before_page.difference(valid_after_rules) != set():
            return False

    return True


def calculate_rules(raw_rules: str) -> tuple[dict[int, set[int], dict[int, set[int]]]]:
    """Calculate the rules."""
    before_rules: dict[int, set[int]] = defaultdict(set[int])
    after_rules: dict[int, set[int]] = defaultdict(set[int])

    for raw_rule in raw_rules.split("\n"):
        left, right = raw_rule.split("|")
        after_rules[int(right)].add(int(left))
        before_rules[int(left)].add(int(right))

    return before_rules, after_rules


def sort_pages(raw_pages: str, before_rules: dict[int, set[int]], after_rules: dict[int, set[int]]) -> int:
    """Sort the pages."""
    pages = [int(page) for page in raw_pages.split(",")]

    sorted_pages = [pages.pop()]

    for page in pages:
        valid_before_rules = before_rules[page].intersection(set(sorted_pages))
        valid_after_rules = after_rules[page].intersection(set(sorted_pages))

        before_indexes = {sorted_pages.index(before_rule) for before_rule in valid_before_rules}
        after_indexes = {sorted_pages.index(after_rule) + 1 for after_rule in valid_after_rules}

        after_indexes.add(0)
        before_indexes.add(0)

        insert_index = max(min(before_indexes), *after_indexes)

        sorted_pages.insert(insert_index, page)

    return sorted_pages[len(sorted_pages) // 2]


def main() -> None:
    """Main function to read input file and calculate the sum of numbers in each line."""
    input_file = Path("./advent_of_code/2024/day05.txt")
    input_data = input_file.read_text()

    raw_rules, raw_pages = input_data.strip().split("\n\n")
    before_rules, after_rules = calculate_rules(raw_rules)

    all_pages = raw_pages.strip().split("\n")
    thing = [check_pages(pages, before_rules, after_rules) for pages in all_pages]

    all_unsorted_pages = [all_pages[index] for index, item in enumerate(thing) if not item]

    print(sum(sort_pages(pages, before_rules, after_rules) for pages in all_unsorted_pages))


if __name__ == "__main__":
    main()
