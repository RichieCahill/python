// _mm_popcnt_u64 For rust
#[no_mangle]
#[inline]
pub extern "C" fn popcnt_u64(mut x: u64) -> u64{
	use std::arch::asm;
	unsafe {
	    asm!(
	        "popcnt {x}, {x}",
					x = inout(reg) x,
	    );
			return x;
	}
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = popcnt_u64(2);
        assert_eq!(result, 1);
        let result = popcnt_u64(3);
        assert_eq!(result, 2);
        let result = popcnt_u64(u64::MAX);
        assert_eq!(result, 64);
    }
}
