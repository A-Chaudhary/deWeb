from pyteal import *
from beaker import sandbox
from base64 import b64decode
import algosdk
from algosdk import transaction

from algosdk.transaction import ApplicationCreateTxn, ApplicationCallTxn, StateSchema, wait_for_confirmation

client = sandbox.get_algod_client()
accounts = sandbox.get_accounts()

def approval_program():
    number = Bytes("number")
    test = Txn.application_args[0]
    init = Seq(
        [
            App.globalPut(number, Int(0)), Approve()
        ]
    )
    create = Seq([
        App.localPut(Txn.sender(), Bytes("txn_id"), test), Approve()
        ]
    )
    
    program = Cond(
        [Txn.application_id() == Int(0), init],
        [Txn.on_completion() == OnComplete.NoOp, create],
        [Txn.on_completion() == OnComplete.OptIn, Approve()],
    )
    return compileTeal(program, mode=Mode.Application, version=8)


def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return b64decode(compile_response['result'])



clear_state_program = compileTeal(
    Approve(),
    mode=Mode.Application,
    version=8
)

signer = accounts[1]
txn = ApplicationCreateTxn(
    sender=signer.address,
    sp=client.suggested_params(),
    on_complete=algosdk.transaction.OnComplete.NoOpOC.real,
    approval_program=compile_program(client, approval_program()),
    clear_program=compile_program(client, clear_state_program),
    global_schema=StateSchema(num_uints=1, num_byte_slices=1),
    local_schema=StateSchema(num_uints=0, num_byte_slices=1),
)



signedTxn = txn.sign(signer.private_key)
txid = client.send_transaction(signedTxn)
response = wait_for_confirmation(client, signedTxn.get_txid(), 4)
print(f"DNS APPLICATION ID IS: {response['application-index']}")

app_id = response['application-index']

app_info = client.application_info(app_id)
app_address = app_info["params"]["creator"]
app_address = algosdk.logic.get_application_address(app_id)






