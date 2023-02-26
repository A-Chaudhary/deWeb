from utilities import zip_webpage, encode_webpage
from beaker import sandbox


#A) given a folder for a static webpage create a zip for that folder 
def publish_webpage(folder):
    INTERMEDIATE = "intermediate.zip"
    zipped = zip_webpage(INTERMEDIATE, folder)
    binarized_zip =  encode_webpage(zipped)



#C) Submit this as a transaction 

#D) Associate this transaction with the name of the webpage and place this webpage onto the view_webpage smart contract


if  __name__ == "__main__":
    client = sandbox.get_algod_client()
    accounts = sandbox.get_accounts()


    pass
