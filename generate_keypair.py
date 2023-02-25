from algosdk import account, mnemonic

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

generate_algorand_keypair()

# My address: HXZ3N3JL3WWW2MQMZHFIV727XI6IGG4R3QL2KRKDNCTR2R5WTXEPE2K7KA
# My private key: XCIJ4EDYC6BbE5nNdC0Wyvm1BNEz0P4SYMoNhZFjfn4987btK92tbTIMycqK/1+6PIMbkdwXpUVDaKcdR7adyA==
# My passphrase: entire cause hybrid lottery bless trend onion october often remind arch original hip donkey ozone south garlic leopard topple express cart ocean view about uncover