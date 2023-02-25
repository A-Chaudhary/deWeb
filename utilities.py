import shutil 
import zipfile
from io import BytesIO
from base64 import b64encode, b64decode
from io import StringIO

def zip_webpage(zip_name, directory_name):
    return shutil.make_archive(zip_name, format='zip', root_dir=directory_name)

def encode_webpage(zip_name):
    with open(zip_name,'rb') as f:
        encoded_bytestring = b64encode(f.read())
    return encoded_bytestring

def decoded_webpage(name_of_zip,encoded_bytestring):
    decoded = b64decode(encoded_bytestring)
    with open(name_of_zip,'wb') as f:
        f.write(decoded)
    
def unzip_webpage(name_of_zip, destination_path):
    shutil.unpack_archive(name_of_zip, destination_path)

if __name__ == "__main__":
    dir_path = "test_webpage"
    destination_path = "output_test_webpage"
    zip_name = zip_webpage("munde",dir_path)
    encoded_bytestring = encode_webpage(zip_name)
    print("Encoded bytestring", encoded_bytestring)
    decoded_webpage("created_zip.zip",encoded_bytestring)
    unzip_webpage("created_zip.zip",destination_path)    