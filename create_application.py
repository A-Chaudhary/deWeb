from pyteal import *
from beaker import sandbox
from base64 import b64decode
import algosdk
from algosdk.transaction import ApplicationCreateTxn, StateSchema, wait_for_confirmation

client = sandbox.get_algod_client()
accounts = sandbox.get_accounts()

def approval_program():
    number = Bytes("number")

    init = Seq(App.globalPut(number, Int(0)), Approve())

    store = Seq(App.globalPut(number, Btoi(Txn.application_args[0])), Approve())

    program = Cond(
        [Txn.application_id() == Int(0), init],
        [Txn.on_completion() == OnComplete.NoOp, store],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.OptIn, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Reject()],
    )
    return compileTeal(program, mode=Mode.Application, version=6)


def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return b64decode(compile_response['result'])



clear_state_program = compileTeal(
    Approve(),
    mode=Mode.Application,
    version=6
)

signer = accounts[0]
txn = ApplicationCreateTxn(
    sender=signer.address,
    sp=client.suggested_params(),
    on_complete=algosdk.transaction.OnComplete.NoOpOC.real,
    approval_program=compile_program(client, approval_program()),
    clear_program=compile_program(client, clear_state_program),
    global_schema=StateSchema(num_uints=1, num_byte_slices=1),
    local_schema=StateSchema(num_uints=0, num_byte_slices=0),
)

signedTxn = txn.sign(signer.private_key)
txid = client.send_transaction(signedTxn)
response = wait_for_confirmation(client, signedTxn.get_txid(), 4)
print(f"Created App with id: {response['application-index']}  in tx: {txid}")


