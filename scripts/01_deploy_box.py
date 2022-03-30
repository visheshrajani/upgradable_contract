from brownie import Box, ProxyAdmin, accounts, TransparentUpgradeableProxy, Contract, BoxV2
from .utils import get_account, encode_function_data, upgrade

def main():
    deploy_box()

def deploy_box():
    account = get_account()
    box = Box.deploy({"from":account})
    proxy_admin = ProxyAdmin.deploy({"from":account})
    box_initializer_func = encode_function_data(box.store,2)
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_initializer_func,
        {"from":account, "gas_limit":1000000}
    )

    proxy_box = Contract.from_abi("Box",proxy.address, box.abi)

    print(proxy_box.retrieve())

    boxv2 = BoxV2.deploy({"from":account})
    tx = upgrade(account, proxy, boxv2.address, proxy_admin)
    tx.wait(1)

    proxy_box = Contract.from_abi("BoxV2",proxy.address, boxv2.abi)

    proxy_box.increment({"from":account})

    print(proxy_box.retrieve())


