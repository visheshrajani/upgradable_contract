from brownie import network, accounts, config
import eth_utils

LOCAL = ["development","ganache-local"]
FORK = ["mainnet-fork"]

def get_account(id=None):
    if id:
        return accounts[id]
    if network.show_active() in LOCAL or network.show_active() in FORK:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def encode_function_data(initializer=None, *args):
    if len(args)==0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    else:
        return initializer.encode_input(*args)

def upgrade(
    account, 
    proxy,
    new_implementation_address, 
    proxy_admin=None, 
    initializer=None, 
    *args
):
    if proxy_admin:
        if initializer:
            encoded_func = encode_function_data(initializer,*args)
            tx = proxy_admin.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_func,
                {"from":account}
            )
        else:
            tx = proxy_admin.upgrade(
                proxy.address,
                new_implementation_address,
                {"from":account}
            )
    else:
        if initializer:
            encoded_func = encode_function_data(initializer,*args)
            tx = proxy.upgradeToAndCall(
                new_implementation_address,
                encoded_func,
                {"from":account}
            )
        else:
            tx = proxy.upgradeTo(
                new_implementation_address,
                {"from":account}
            )
    return tx