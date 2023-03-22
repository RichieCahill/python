import tarfile
from zstandard import ZstdCompressor
from io import BytesIO
from cryptography.fernet import Fernet

source_dir = "./TestDIR"

tar_bytes = BytesIO()
with tarfile.open(fileobj=tar_bytes, mode="w:tar") as tar:
	tar.add(source_dir)

compressed_data = ZstdCompressor(level=22, write_checksum=True, write_content_size=True, threads=8).compress(tar_bytes.getvalue())

key = b"FADvU5pm87FM1ImNeyAK3ZqNRLlqIAKNKmaYHnt5mVU="
encrypted_bytes = Fernet(key).encrypt(compressed_data)

with open("./archive.tar.zst.encrypted", "wb") as f:
    f.write(encrypted_bytes)

# TODO
# Upload file to azure
# Hash the output file and save?
