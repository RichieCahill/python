from  ctypes import cdll, c_uint64

rust_lib = cdll.LoadLibrary("./target/release/libpython_asm.so")

# set the input and output parameters
rust_lib.popcnt_u64.argtype = c_uint64
rust_lib.popcnt_u64.restype = c_uint64

from random import randint

test_dict = {18446744073709551615: 64}

for _ in range(100_000_000):
	test = 18446744073709551615
	result1 = rust_lib.popcnt_u64(test)
	result2 = test.bit_count()
	result3 = test_dict.get(test)

# print(random_number)
print(test)
print(result1)
print(result2)
print(result3)

# for _ in range(100_000_000):
# 	test = 1
# 	result1 = rust_lib.popcnt_u64(test)
# 	result2 = test.bit_count()

# # print(random_number)
# print(test)
# print(result1)
# print(result2)
