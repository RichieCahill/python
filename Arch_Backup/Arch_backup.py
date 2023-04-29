import logging
import logging.config
from cryptography.fernet import Fernet
from io import BytesIO
from json import load
from subprocess import Popen, PIPE
from tarfile import open as taropen
from TMMPythonPackage import TypeTest, GetLoggerDict
from zstandard import ZstdCompressor
from datetime import datetime
from time import sleep
from os import chown, remove
from hashlib import sha512
from random import random 

logging.config.dictConfig(GetLoggerDict("DEBUG","./Log/Arch_Info.log"))
logging.getLogger("default")

def BashWrapper(command: str):
	TypeTest(command, test_type=str, error_msg=f"command type = {command} should be str")
	process = Popen(command.split(), stdout=PIPE)
	output ,error = process.communicate()
	return output.decode(), process.returncode

def TrueBashWrapper(command: str):
	TypeTest(command, test_type=str, error_msg=f"command type = {command} should be str")
	process = Popen(command, shell=True, stdout=PIPE)
	output ,error = process.communicate()
	return output.decode(), process.returncode

def PingTest(host: str, number_of_attempts: int = 60, delay: int = 5) -> bool:
	TypeTest(host, test_type=str, error_msg=f"host is {host} should be str")
	TypeTest(host, test_type=str, error_msg=f"host is {host} should be str")
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

def ArchiveDir(dir_name: str, output_file: str, encryption_key: str):
	TypeTest(dir_name, test_type=str, error_msg=f"dir_name type is {type(dir_name)} should be str")

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

	working_dir = "/etc/"
	temp_file = f"/tmp/{sha512(str(random()).encode()).hexdigest()}"
	output_file = f"/ZFS/Storage/Backups/BOB/etc_{Now.strftime('%Y-%m-%d-%M')}.tar.zst.encrypted"

	# gets all pacman packages
	GetPackageList(command = "pacman -Qent",output_file = f'{working_dir}pacman_list.cvs' )
	# gets all yay packages
	GetPackageList(command = "pacman -Qmt",output_file = f'{working_dir}yay_list.cvs')

	# TODO replace with a key vault
	key = get_key("./secret.json")

	ArchiveDir(working_dir, temp_file, key)
	print(PingTest(host = "192.168.99.40"))

	chown(temp_file, 1000, 1000)

	_, returncode = TrueBashWrapper(f"runuser -l r2r0m0c0 -c 'cp {temp_file} {output_file}'")
	if returncode != 0:
		logging.critical(f"backup FAILED returncode = {returncode}")
	remove(temp_file)

	logging.info("arch_backup DONE")

if __name__ == "__main__":
	arch_backup()
