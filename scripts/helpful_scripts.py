from brownie import accounts, network, config
import eth_utils

Local_Blockchain_Environments = ["development", "ganache-local"]
Forked_Environments = ["mainnet-fork", "moonriver-fork"]


def getAccount(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)  # Select specific account based on its id or index

    if (
        network.show_active()
        in Local_Blockchain_Environments  # If using local chain, use the first address provided from that chain
        or network.show_active() in Forked_Environments
    ):
        return accounts[0]
    return accounts.add(  # Otherwise, use wallet associated with current network
        config["wallets"]["from_key"]
    )


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(account, proxy, new_imp_address, proxy_admin=None, initializer=None, *args):
    if proxy_admin:
        if initializer:
            encoded_function_data = encode_function_data(initializer, *args)
            tx = proxy_admin.upgradeAndCall(
                proxy.address,
                new_imp_address,
                encoded_function_data,
                {"from": account},
            )
        else:
            tx = proxy_admin.upgrade(proxy.address, new_imp_address, {"from": account})
    else:
        if initializer:
            encoded_data = encode_function_data(initializer, *args)
            tx = proxy.upgradeToAndCall(
                new_imp_address, encoded_data, {"from": account}
            )
        else:
            tx = proxy.upgradeTo(new_imp_address, {"from": account})
    return tx
