from pyteal import *
from beaker import sandbox
from base64 import b64decode
from algosdk.transaction import LogicSigAccount
import algosdk


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

logic_sig_teal = compileTeal(ValidateRecord("ans"), Mode.Signature, version=5)

compiled_logic_sig_teal = compile_program(algod_client, logic_sig_teal)

lsig = LogicSigAccount(compiled_logic_sig_teal)

print(lsig.address())

# Creating an optin txn

optin_txn_unsigned = algosdk.transaction.ApplicationOptInTxn(lsig.address(), algod_client.suggested_params(), 1)

# Signing the optin txn

optin_signed_txn = algosdk.transaction.LogicSigTransaction(optin_txn_unsigned, lsig)

# Send txn to network

algod_client.send_transaction(optin_signed_txn)
