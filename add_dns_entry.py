from pyteal import *
from beaker import sandbox
from base64 import b64decode
from algosdk.transaction import LogicSigAccount
from algosdk.transaction import ApplicationCreateTxn, ApplicationCallTxn, StateSchema, wait_for_confirmation

import algosdk
from algosdk import transaction

from utilities import zip_webpage, encode_webpage
from beaker import sandbox



def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return b64decode(compile_response['result'])
algod_client = sandbox.get_algod_client()

def ValidateRecord(name):
    program = Cond(
        [Len(Bytes(name)) >= Int(3), Return(Int(1))]
    )
    return program

def approval_program():

    optin_to_app = Seq([
        App.localPut(Int(0), Bytes("registered"), Int(1)),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), Return(Int(1))],
        [Txn.on_completion() == OnComplete.OptIn, optin_to_app]
    )

    return program

def clear_state_program():
    return Int(0)     

domain = input("Enter domain name: ")
logic_sig_teal = compileTeal(ValidateRecord(domain), Mode.Signature, version=5)

compiled_logic_sig_teal = compile_program(algod_client, logic_sig_teal)

lsig = LogicSigAccount(compiled_logic_sig_teal)
app_id = input("ENTER DNS APPLICATION ID: ")

accounts = sandbox.get_accounts()
account = accounts[1]

unsigned_txn = transaction.PaymentTxn(account.address, algod_client.suggested_params(), lsig.address(), 1000000, None, None)
signed_txn = unsigned_txn.sign(account.private_key)
txid = algod_client.send_transaction(signed_txn)
confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  


INTERMEDIATE = "intermediate.zip"
zipped = zip_webpage(INTERMEDIATE, "input")
binarized_zip =  encode_webpage(zipped)


unsigned_txn = transaction.PaymentTxn(account.address, algod_client.suggested_params(), lsig.address(), 1, None, binarized_zip)
signed_txn = unsigned_txn.sign(account.private_key)
txid = algod_client.send_transaction(signed_txn)
confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  


# Creating an optin txn
optin_txn_unsigned = algosdk.transaction.ApplicationOptInTxn(lsig.address(), algod_client.suggested_params(), app_id)

# Signing the optin txn

optin_signed_txn = algosdk.transaction.LogicSigTransaction(optin_txn_unsigned, lsig)

# Send txn to network

algod_client.send_transaction(optin_signed_txn)

txn = ApplicationCallTxn(
    sender=lsig.address(),
    sp=algod_client.suggested_params(),
    index=app_id,
    app_args=[txid],
    on_complete=algosdk.transaction.OnComplete.NoOpOC,
)
signedTxn = algosdk.transaction.LogicSigTransaction(txn, lsig)

txid = algod_client.send_transaction(signedTxn)
response = wait_for_confirmation(algod_client, signedTxn.get_txid(), 4)

results = algod_client.application_info(app_id)

