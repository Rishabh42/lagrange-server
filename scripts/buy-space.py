"""Manual transfer script for space payment.

- Will transfer 1 LAD every epoch for 10000 epochs

"""
import time
import sys
import os
import json

from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware


from dotenv import load_dotenv

load_dotenv()

rpc_endpoint = os.getenv("rpc_endpoint")
assert rpc_endpoint is not None, "You must set rpc_endpoint in .env file"
web3 = Web3(HTTPProvider(rpc_endpoint))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
block_number = web3.eth.block_number
print(f"Connected to blockchain, chain id is {web3.eth.chain_id}. the latest block is {block_number:,}\n")

epoch_time = 15

space_contract_address = "0x7a5eE2b7438c46eab9890E48feB18F8ef69D978e"
space_abi_file = open('SpacePayment.json')
space_abi = json.load(space_abi_file)

token_contract_address = "0x31174CE312C34b64eaf75d97bA0cfbEb28E4B45D"
token_abi_file = open('LagrangeDAOToken.json')
token_abi = json.load(token_abi_file)

wallet_address = os.getenv('wallet_address')
private_key = os.getenv('private_key')

assert web3.isChecksumAddress(wallet_address), f"Not a valid wallet address: {wallet_address}"
assert web3.isChecksumAddress(space_contract_address), f"Not a valid contract address: {space_contract_address}"
assert web3.isChecksumAddress(token_contract_address), f"Not a valid contract address: {space_contract_address}"

# Show users the current status of token and his address
space_contract = web3.eth.contract(address=space_contract_address, abi=space_abi)
token_contract = web3.eth.contract(address=token_contract_address, abi=token_abi)
token_name, token_symbol = token_contract.functions.name().call(), token_contract.functions.symbol().call()
token_decimals = token_contract.functions.decimals().call()
# print(f"Token: {token_name} ({token_symbol})")

token_balance = token_contract.functions.balanceOf(wallet_address).call()

# native_balance = web3.eth.getBalance(wallet_address)

print(f"wallet address: {wallet_address}")
print(f"account balance: {token_balance/(10**token_decimals):,} {token_symbol}")
print(f"epoch time: 1 block per {epoch_time} seconds\n")

hardware_type = input(" 1. CPU Only - 2 vCPU - 16 GiB - Free \
    \n 2. CPU Only - 8 vCPU - 32 GiB - $0.03 per hour - 1 LAD per block \
    \n 3. Nvidia T4 - 4 vCPU - 15 GiB - $0.60 per hour - 20 LAD per block \
    \n 4. Nvidia T4 - 8 vCPU - 30 GiB - $0.90 per hour - 30 LAD per block \
    \n 5. Nvidia A10G - 4 vCPU - 15 GiB - $1.05 per hour - 35 LAD per block \
    \n 6. Nvidia A10G - 12 vCPU - 46 GiB - $3.15 per hour - 105 LAD per block \
    \n\nSelect the hardware (#): ")

hours = input("How many hours: ")
blocks = float(hours) * 60 * 60 / epoch_time

# Fat-fingering check
print(f"Confirm purchasing hardware type {hardware_type} for {hours} hours ({blocks} blocks)?")
confirm = input("Ok [y/n]?")
if not confirm.lower().startswith("y"):
    print("Aborted")
    sys.exit(1)

prices = [0, 1, 20, 30, 35, 105]
price = prices[int(hardware_type) - 1] * blocks

print(f"\ndepositing {price} {token_symbol} into contract...")
nonce = web3.eth.getTransactionCount(wallet_address)
approve_tx = token_contract.functions.approve(space_contract_address, int(price) * 10**token_decimals).buildTransaction({
    'from': wallet_address,
    'nonce': nonce
})

# SIGN TX
signed_tx = web3.eth.account.signTransaction(approve_tx, private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
web3.eth.wait_for_transaction_receipt(tx_hash)
hash = web3.toHex(tx_hash)

nonce = web3.eth.getTransactionCount(wallet_address)
deposit_tx = space_contract.functions.deposit(int(price) * 10**token_decimals).buildTransaction({
    'from': wallet_address,
    'nonce': nonce
})

# SIGN TX
signed_tx = web3.eth.account.signTransaction(deposit_tx, private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
web3.eth.wait_for_transaction_receipt(tx_hash)
hash = web3.toHex(tx_hash)

print(f"transaction hash: {hash}")


print(f"\npurchasing space...")
nonce = web3.eth.getTransactionCount(wallet_address)
tx = space_contract.functions.buySpace(int(hardware_type), int(blocks)).buildTransaction({
    'from': wallet_address,
    'nonce': nonce
})

# SIGN TX
signed_tx = web3.eth.account.signTransaction(tx, private_key)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
web3.eth.wait_for_transaction_receipt(tx_hash)
hash = web3.toHex(tx_hash)

print(f"transaction hash: {hash}")