from algosdk.v2client import algod
import generate_keypair



def first_transaction_example(private_key, my_address):
    algod_address = "http://localhost:4001"
    algod_token = generate_keypair.ADDRESS
    algod_client = algod.AlgodClient(algod_token, algod_address)

if __name__ == "__main__":
    first_transaction_example(generate_keypair.PRIVATE_KEY, generate_keypair.ADDRESS)