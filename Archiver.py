import tarfile
from zstandard import ZstdCompressor
from io import BytesIO

source_dir = "./DIR"

tar_bytes = BytesIO()
with tarfile.open(fileobj=tar_bytes, mode="w:tar") as tar:
	tar.add(source_dir)

compressed_data = ZstdCompressor(level=22).compress(tar_bytes.getvalue())

with open("archive.tar.zst", "wb") as f:
	f.write(compressed_data)
