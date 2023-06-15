while True:
  print("YAY")
  if 1 == 0:
    break
else: #nobreak
	print("YAY")

def or_example(input_data):
	return input_data or "right"

def safe_div2(input_data):
	return input_data and input_data//2
