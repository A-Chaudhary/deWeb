from pyteal import *
from beaker import sandbox
from base64 import b64decode
import algosdk
from algosdk.transaction import ApplicationCreateTxn, ApplicationCallTxn, StateSchema, wait_for_confirmation

client = sandbox.get_algod_client()
accounts = sandbox.get_accounts()

def approval_program():
    number = Bytes("number")
    init = Seq(
        [
            App.globalPut(number, Int(0)), Approve()
        ]
    )
    create = Seq(
        Pop(App.box_create(Bytes("testbox"), Int(100))), Approve()
    )
    program = Cond(
        [Txn.application_id() == Int(0), init],
        [Txn.on_completion() == OnComplete.NoOp, create],
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

signer = accounts[0]
txn = ApplicationCreateTxn(
    sender=signer.address,
    sp=client.suggested_params(),
    on_complete=algosdk.transaction.OnComplete.NoOpOC.real,
    approval_program=compile_program(client, approval_program()),
    clear_program=compile_program(client, clear_state_program),
    global_schema=StateSchema(num_uints=1, num_byte_slices=1),
    local_schema=StateSchema(num_uints=0, num_byte_slices=0),
    boxes=[(0, b"testbox")]
)

print(txn)

signedTxn = txn.sign(signer.private_key)
txid = client.send_transaction(signedTxn)
response = wait_for_confirmation(client, signedTxn.get_txid(), 4)
print(f"Created App with id: {response['application-index']}  in tx: {txid}")

app_id = response['application-index']
txn = ApplicationCallTxn(
    sender=accounts[0].address,
    sp=client.suggested_params(),
    index=app_id,
    on_complete=algosdk.transaction.OnComplete.NoOpOC,
    app_args=[5],   
    boxes=[(0, b"testbox")]
)

signedTxn = txn.sign(accounts[0].private_key)
txid = client.send_transaction(signedTxn)
response = wait_for_confirmation(client, signedTxn.get_txid(), 4)
