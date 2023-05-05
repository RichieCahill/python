import logging
import logging.config
from cryptography.fernet import Fernet
from datetime import datetime
from hashlib import sha512
from io import BytesIO
from json import load
from os import chown, remove
from random import random 
from tarfile import open as taropen
from time import sleep
from TMMPythonPackage import GetLoggerDict, TypeTest, BashWrapper, TrueBashWrapper 
from zstandard import ZstdCompressor

logging.dictConfig(GetLoggerDict("DEBUG","./Log/Arch_Info.log"))
logging.getLogger("default")

def PingTest(
	host:  str, 
	delay: int = 5,
	number_of_attempts: int = 60,
	) -> bool:
	TypeTest(delay, test_type=int, error_msg=f"delay is {delay} should be int")
	TypeTest(host, test_type=str, error_msg=f"host is {host} should be str")
	TypeTest(number_of_attempts, test_type=int, error_msg=f"number_of_attempts is {number_of_attempts} should be int")
	for _ in range(number_of_attempts):
		_, returncode = BashWrapper(f"ping -c 1 {host}")
		if returncode == 0:
			return True
		sleep(delay)
	return False

def GetPackageList(command: str, output_file: str):
	logging.info(f"running GetPackageList {command}")
	TypeTest(command, str, f"command = {command} should be str")
	TypeTest(output_file, str, f"output_file = {output_file} should be str")

	command_output, returncode = BashWrapper(command)
	if returncode != 0:
		logging.debug(returncode)
		logging.error(f"GetPackageList {command} failed")
		return
	with open(output_file, 'w') as f:
		f.write(command_output.replace(" ", ","))
	logging.info("GetPackageList done")

def ArchiveDir(
	dir_name: str,
	encryption_key: str,
	output_file: str,
	):
	TypeTest(dir_name, test_type=str, error_msg=f"dir_name type is {dir_name} should be str")
	TypeTest(encryption_key, test_type=str, error_msg=f"encryption_key type is {encryption_key} should be str")
	TypeTest(output_file, test_type=str, error_msg=f"output_file type is {output_file} should be str")

	tar_bytes = BytesIO()
	with taropen(fileobj=tar_bytes, mode="w:tar") as tar:
		tar.add(dir_name)

	zstd_settings = ZstdCompressor(level=22, write_checksum=True, write_content_size=True, threads=8)

	compressed_data = zstd_settings.compress(tar_bytes.getvalue())

	encrypted_bytes = Fernet(encryption_key).encrypt(compressed_data)

	with open(output_file, "wb") as f:
			f.write(encrypted_bytes)

def get_key(file):
	# Open the JSON file in read mode
	with open(file, 'r') as f:
		data = load(f)
	key = data.get("key")
	if key:
		return key
	raise ValueError("Failed to load key")
 
def arch_backup():
	logging.info("arch_backup STARTING")
	Now = datetime.now()

	uid = 1000
	gid = 1000
	host = "192.168.99.40"
	archive_dir = "/etc/"
	temp_file = f"/tmp/{sha512(str(random()).encode()).hexdigest()}"
	output_file = f"/ZFS/Storage/Backups/BOB/etc_{Now.strftime('%Y-%m-%d')}.tar.zst.encrypted"

	# gets all pacman packages
	GetPackageList(command = "pacman -Qent", output_file = f'{archive_dir}pacman_list.cvs' )
	# gets all yay packages
	GetPackageList(command = "pacman -Qmt", output_file = f'{archive_dir}yay_list.cvs')

	# TODO replace with a key vault
	key = get_key("./secret.json")

	ArchiveDir(archive_dir, temp_file, key)
	print(PingTest(host = host))

	chown(path=temp_file, uid=uid, gid=gid)

	_, returncode = TrueBashWrapper(f"runuser -l r2r0m0c0 -c 'cp {temp_file} {output_file}'")
	if returncode != 0:
		logging.critical(f"backup FAILED returncode = {returncode}")
	remove(temp_file)

	logging.info("arch_backup DONE")

if __name__ == "__main__":
	arch_backup()
