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

logging.config.dictConfig(GetLoggerDict("DEBUG","./Log/Arch_Info.log"))
logging.getLogger("default")

def BashWrapper(command: str):
	TypeTest(command, test_type=str, error_msg=f"command type is {type(command)} should be str")
	process = Popen(command.split(), stdout=PIPE)
	output ,error = process.communicate()
	return output.decode(), error

def get_package_list(command: str, output_file: str):
	logging.info(f"running get_package_list {command}")
	TypeTest(command, test_type=str, error_msg=f"command type is {type(command)} should be str")
	TypeTest(output_file, test_type=str, error_msg=f"output_file type is {type(output_file)} should be str")

	command_output = BashWrapper(command)
	if command_output[1]:
		logging.debug(command_output[1])
		print(command_output[1])
		logging.error(f"get_package_list {command} failed")
		return
	with open(output_file, 'w') as f:
		f.write(command_output[0].replace(" ", ","))
	logging.info("get_package_list done")

def archive_dir(dir_name: str, output_file: str, encryption_key: str):
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
	try:
		logging.info("arch_backup STARTING")
		Now = datetime.now()
		working_dir = "/etc/"

		# gets all pacman packages
		get_package_list(command = "pacman -Qent",output_file = working_dir + 'pacman_list.cvs' )
		# gets all yay packages
		get_package_list(command = "pacman -Qmt",output_file = working_dir + 'yay_list.cvs')
		# TODO replace with a key vault
		key = get_key("./secret.json")
		archive_dir(working_dir, f"/tmp/etc_{Now.strftime('%Y-%m-%d')}.tar.zst.encrypted", key)
		logging.info("arch_backup DONE")
	except Exception as err:
		logging.critical(err)
		exit(1)
 

if __name__ == "__main__":
	arch_backup()
