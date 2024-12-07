"""DAY1_Part1"""

from collections import defaultdict
from pathlib import Path


def check_pages(raw_pages: str, before_rules: dict[int, set[int]], after_rules: dict[int, set[int]]) -> int:
    """Check the pages."""
    pages = [int(page) for page in raw_pages.split(",")]
    for index, page in enumerate(pages):
        pages_after_page = set(pages[index + 1 :])
        valid_before_rules = before_rules[page].intersection(pages_after_page)
        if len(valid_before_rules) != 0 and pages_after_page.difference(valid_before_rules) != set():
            return 0

        pages_before_page = set(pages[:index])
        valid_after_rules = after_rules[page].intersection(pages_before_page)
        if len(valid_after_rules) != 0 and pages_before_page.difference(valid_after_rules) != set():
            return 0

    return pages[len(pages) // 2]


def calculate_rules(raw_rules: str) -> tuple[dict[int, set[int], dict[int, set[int]]]]:
    """Calculate the rules."""
    before_rules: dict[int, set[int]] = defaultdict(set[int])
    after_rules: dict[int, set[int]] = defaultdict(set[int])

    for raw_rule in raw_rules.split("\n"):
        left, right = raw_rule.split("|")
        before_rules[int(left)].add(int(right))
        after_rules[int(right)].add(int(left))

    return before_rules, after_rules


def main() -> None:
    """Main function to read input file and calculate the sum of numbers in each line."""
    input_file = Path("./advent_of_code/2024/day05.txt")
    input_data = input_file.read_text()

    raw_rules, raw_pages = input_data.strip().split("\n\n")
    before_rules, after_rules = calculate_rules(raw_rules)

    all_pages = raw_pages.strip().split("\n")

    print(sum(check_pages(pages, before_rules, after_rules) for pages in all_pages))


if __name__ == "__main__":
    main()
