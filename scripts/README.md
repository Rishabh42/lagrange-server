# Transfer Scripts

This folder contains Python scripts to transfer ERC-20 tokens.

## Set up

### Install Packages:

```
pip install web3 python-dotenv
```

### Create your own .env

copy _.env.template_ to _.env_

```
wallet_address = " "
private_key = " "
rpc_endpoint = "https://polygon-rpc.com"
SQLALCHEMY_DATABASE_URI="mysql+pymysql://user:pass@127.0.0.1:3306/lagrange"
DOMAIN="127.0.0.1"
```

update the file with your own values.

### Before Running

The current `token_contract_address` and `space_contract_address` are deployed on the Mumbai network. To deploy your own, follow the instructions in the `../hardhat` folder

You will need some LAD tokens to run the script successfully.

## Running

Run the script:

```
python buy-space.py
```

Example output

```
Connected to blockchain, chain id is 80001. the latest block is 31,028,769

wallet address: 0xA878795d2C93985444f1e2A077FA324d59C759b0
account balance: 149,990,287.0 LAD
epoch time: 1 block per 15 seconds

 1. CPU Only - 2 vCPU - 16 GiB - Free
 2. CPU Only - 8 vCPU - 32 GiB - $0.03 per hour - 1 LAD per block
 3. Nvidia T4 - 4 vCPU - 15 GiB - $0.60 per hour - 20 LAD per block
 4. Nvidia T4 - 8 vCPU - 30 GiB - $0.90 per hour - 30 LAD per block
 5. Nvidia A10G - 4 vCPU - 15 GiB - $1.05 per hour - 35 LAD per block
 6. Nvidia A10G - 12 vCPU - 46 GiB - $3.15 per hour - 105 LAD per block

Select the hardware (#): 3
How many hours: 0.5
Confirm purchasing hardware type 3 for 0.5 hours (120.0 blocks)?
Ok [y/n]?y

depositing 2400.0 LAD into contract...
transaction hash: 0xd51309d7a951602b879b8ea1c8189d1eb7d211d5d43f3c0c938ebfcd4b434db9

purchasing space...
transaction hash: 0x7be13c16c175f690dc9883298aa6c6a57058b649038d73f12bf80cdf0b883bdb
```
