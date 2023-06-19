"""
Some of the pairs have noticed that one of their assignments fully contains the other.
For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6.
In pairs where one assignment fully contains the other,
one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning,
so these seem like the most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?
"""

def split_dash(side: str):
	right, left = side.split("-")
	if right == left:
		return {int(right),}
	return set(range(int(right), int(left)+1))

def check_overlap(left_side, right_side):
	return left_side.issubset(right_side) or right_side.issubset(left_side)

def camp_cleanup(rows):
	result = 0
	for row in rows:
		left_side, right_side = row.split(",")
		if check_overlap(
			left_side=split_dash(left_side),
			right_side=split_dash(right_side)
		):
			result += 1
	return result

def camp_cleanup_part2(rows):
	result = 0
	for row in rows:
		left_side, right_side = row.split(",")
		if(split_dash(left_side).intersection(split_dash(right_side))):
			result += 1
	return result

def main():
	with open("./DAY4.txt", "r") as file:
		input_file = [line.strip() for line in file]

	result = camp_cleanup(input_file)
	print(result)

	result = camp_cleanup_part2(input_file)
	print(result)

main()