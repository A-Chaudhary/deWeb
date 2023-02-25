import shutil 
        
def zip_webpage(zip_name, directory_name):
    return shutil.make_archive(zip_name, format='zip', root_dir=directory_name)

def unzip_webpage(zip_directory_name, destination_path):
    shutil.unpack_archive(zip_directory_name, destination_path)

if __name__ == "__main__":
    dir_path = "test_webpage"
    destination_path = "output_test_webpage"
    zipped = zip_webpage("munde",dir_path)
    print(zipped)
    unzip_webpage = unzip_webpage(zipped,destination_path=destination_path)   
    