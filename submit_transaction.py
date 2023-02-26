from algosdk import account, mnemonic
from algosdk.v2client import algod
import json, base64
from algosdk import transaction
from algosdk import constants

ADDRESS = "4U5ORBQYAKHPRQXP3Z2CKPVB2XZFRFUQGD5F4S23VHB6RB3JCZDXEHFY6E"
PRIVATE_KEY = "YRq1VZmyteqrT6o+LzPfyIWv0E/vV76OT6+FU+ZcamrlOuiGGAKO+MLv3nQlPqHV8liWkDD6XktbqcPoh2kWRw=="
PASSPHRASE = "equip stamp print civil hidden wide later prevent treat smile hurdle frame gallery vintage kidney fitness style dilemma stumble debate smile now fashion about hood"

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    passphrase = mnemonic.from_private_key(private_key)
    print("My passphrase: {}".format(passphrase))
    return (address, private_key, passphrase)

def connect_to_client():
    algod_address ="http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)
    return algod_client

def check_balance(algod_client):
    account_info = algod_client.account_info(ADDRESS)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
    return account_info

def build_transaction(algod_client, private_key, my_address, byte_string):
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = constants.MIN_TXN_FEE 
    receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    note = byte_string
    amount = 1000000
    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)
    signed_txn = unsigned_txn.sign(private_key)

    return signed_txn, amount, params



def submit_transction(algod_client, signed_txn, amount, params, my_address, account_info):
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 
    account_info = algod_client.account_info(my_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")


def submit_tx(byte_string):
    algod_client = connect_to_client()
    account_info = check_balance(algod_client = algod_client)
    signed_txn, amount, params = build_transaction(algod_client, PRIVATE_KEY, ADDRESS, byte_string)
    submit_transction(algod_client, signed_txn, amount, params, ADDRESS, account_info)


if __name__ == "__main__":
    submit_tx()
