from  ctypes import cdll, c_uint64

rust_lib = cdll.LoadLibrary("./target/release/libpython_asm.so")

# set the input and output parameters
rust_lib.popcnt_u64.argtype = c_uint64
rust_lib.popcnt_u64.restype = c_uint64

result = rust_lib.popcnt_u64(1)
print(f"1 popcnt_u64 = {result}")
result = rust_lib.popcnt_u64(3)
print(f"3 popcnt_u64 = {result}")
result = rust_lib.popcnt_u64(18446744073709551615)
print(f"18446744073709551615 popcnt_u64 = {result}")
