"""
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

		The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, 
		which means its first compartment contains the items vJrwpWtwJgWr, 
		while the second compartment contains the items hcsFMMfFFhFp.
		The only item type that appears in both compartments is lowercase p.
		The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is uppercase L.
		The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.
		The fourth rucksack's compartments only share item type v.
		The fifth rucksack's compartments only share item type t.
		The sixth rucksack's compartments only share item type s.

To help prioritize item rearrangement, every item type can be converted to a priority:

		Lowercase item types a through z have priorities 1 through 26.
		Uppercase item types A through Z have priorities 27 through 52.

In the above example, the priority of the item type that appears in both compartments of each rucksack is
16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack.
What is the sum of the priorities of those item types?
"""

def rucksack_reorganization(rucksacks: list, values: list):

	result = 0
	for rucksack in rucksacks:

		rucksack_mid = len(rucksack)//2
		rucksack_first, rucksack_second = rucksack[:rucksack_mid], rucksack[rucksack_mid:]

		intersect = set(rucksack_first).intersection(set(rucksack_second))

		result = result + values.index(intersect.pop())
	 
	return result

from more_itertools import chunked
def rucksack_reorganization_part2(rucksacks: list, values: list):

 
	rucksack_groups = list(chunked(rucksacks, 3))
 
	result = 0
	for rucksack1, rucksack2, rucksack3 in rucksack_groups:

		intersect = set(rucksack1).intersection(set(rucksack2), set(rucksack3))

		result = result + values.index(intersect.pop())

	return result

def main():
	with open("./DAY3.txt", "r") as file:
		input_file = [line.strip()	for line in file]

	values = "0 a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()

	result = rucksack_reorganization(input_file, values)
	print(result)

	result = rucksack_reorganization_part2(input_file, values)
	print(result)


main()
