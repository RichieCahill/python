"""
For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y).
This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X).
This ends in a loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors,
giving you a score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).
"""

def rock_paper_scissors(games):

  table = {
    "A X": 4,
    "A Y": 8,
    "A Z": 3,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 7,
    "C Y": 2,
    "C Z": 6
  }

  results = [table.get(game) for game in games]    

  return sum(results)

# this is slower probly becaus of the size of the data set but uses less memory
def rock_paper_scissors_dict_1(games):

  table = {
    "A X": 4,
    "A Y": 8,
    "A Z": 3,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 7,
    "C Y": 2,
    "C Z": 6
  }

  return sum(table.get(game) for game in games)

# this is slower probly becaus of the size of the data set but uses less memory

def rock_paper_scissors_dict_2(games):
  return sum([{"A X": 4,"A Y": 8,"A Z": 3,"B X": 1,"B Y": 5,"B Z": 9,"C X": 7,"C Y": 2,"C Z": 6}.get(game) for game in games])

# This is faster on the dataset for some reasion
def rock_paper_scissors_dict_3(games):

  table = {
    "B X": 1,
    "C Y": 2,
    "A Z": 3,
    "A X": 4,
    "B Y": 5,
    "C Z": 6,
    "C X": 7,
    "A Y": 8,
    "B Z": 9,
  }

  results = [table.get(game) for game in games]    

  return sum(results)

def rock_paper_scissors_list(games):

  table = (None, "B X", "C Y", "A Z", "A X", "B Y", "C Z", "C X", "A Y", "B Z")

  results = [table.index(game) for game in games]    

  return sum(results)

def rock_paper_scissors_part2(games):

  table = {
    "A X": 3+0,
    "A Y": 1+3,
    "A Z": 2+6,
    "B X": 1+0,
    "B Y": 2+3,
    "B Z": 3+6,
    "C X": 2+0,
    "C Y": 3+3,
    "C Z": 1+6 
  }

  results = [table.get(game) for game in games]    

  return sum(results)


def main():
  with open("./DAY2.txt", "r") as file:
    input_file = [line.strip()  for line in file]
  num = 1000
  for _ in range(num):
    result = rock_paper_scissors_dict_3(input_file)
  print(result)
  for _ in range(num):
    result = rock_paper_scissors(input_file)
  print(result)

  result = rock_paper_scissors_part2(input_file)
  print(result)

main()
