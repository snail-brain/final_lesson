from brownie import TokenFarm, network, config, DappToken
from scripts.helpful_scripts import *

account = getAccount()


def main():
    print("Deploying Dapp Token")
    token = DappToken.deploy({"from": account})

    weth_amount = weth.balanceOf(account.address)
    dai_amount = dai.balanceOf(account.address)

    print("Deploying Token Farm")
    farm = TokenFarm.deploy(token.address, {"from": account})
    token.transfer(farm.address, token.balanceOf(account.address))

    farm.addAllowedToken(
        weth.address,
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )

    farm.addAllowedToken(
        dai.address,
        config["networks"][network.show_active()]["dai_usd_price_feed"],
        {"from": account},
    )

    print("Approving wETH for transfer")
    weth.approve(farm.address, weth_amount, {"from": account})
    print("Approving Dai for transfer")
    dai.approve(farm.address, dai_amount, {"from": account})

    print("Staking wETH")
    farm.stakeTokens(weth_amount, weth.address, {"from": account})
    print("Staking Dai")
    farm.stakeTokens(dai_amount, dai.address, {"from": account})

    print(weth.balanceOf(farm.address))
    print(dai.balanceOf(farm.address))

    print(
        f"Your current staked TVL in usd: {farm.findUserTVL(account.address) / 10 ** 18}"
    )

    print("Issuing Tokens")
    farm.issueTokens({"from": account})
    print(
        f"DappToken Balance: {token.balanceOf(account.address) / 10 ** token.decimals()}"
    )

    print("Unstaking Tokens")
    farm.unstake(weth.address, weth_amount, {"from": account})
    farm.unstake(dai.address, dai_amount, {"from": account})

    print(f"Your wETH Balance: {weth.balanceOf(account.address)}")
    print(f"Your Dai Balance: {dai.balanceOf(account.address)}")
