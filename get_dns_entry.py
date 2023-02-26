from pyteal import *
from beaker import sandbox
from base64 import b64decode
from algosdk.transaction import LogicSigAccount
from algosdk.transaction import ApplicationCreateTxn, ApplicationCallTxn, StateSchema, wait_for_confirmation
import base64
import algosdk
from algosdk import transaction


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

def get_domain_tx(domain):
    logic_sig_teal = compileTeal(ValidateRecord(domain), Mode.Signature, version=5)

    compiled_logic_sig_teal = compile_program(algod_client, logic_sig_teal)

    lsig = LogicSigAccount(compiled_logic_sig_teal)


    # RETRIEVE DNS
    results = algod_client.account_info(lsig.address())
    local_state = results
    return base64.b64decode(local_state['apps-local-state'][0]['key-value'][0]['value']['bytes']).decode()