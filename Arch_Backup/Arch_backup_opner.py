import logging
import logging.config
from cryptography.fernet import Fernet
from json import load
from TMMPythonPackage import GetLoggerDict

logging.config.dictConfig(GetLoggerDict("DEBUG","./Log/Arch_Info.log"))
logging.getLogger("default")

def get_key(file):
	# Open the JSON file in read mode
	with open(file, 'r') as f:
			data = load(f)
	key = data.get("key")
	if key:
		return key
	raise ValueError("Failed to load key")
 

from cryptography.fernet import Fernet

# Load the encrypted file
with open('./archive.tar.zst.encrypted', 'rb') as f:
    encrypted_data = f.read()

key = get_key("./secret.json")
f = Fernet(key)

# Decrypt the data
decrypted_data = f.decrypt(encrypted_data)

# Write the decrypted data to a file
with open('./archive.tar.zst', 'wb') as f:
    f.write(decrypted_data)
