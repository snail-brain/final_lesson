from brownie import TokenFarm, DappToken, config, network, Contract
from scripts.helpful_scripts import *
import json


account = getAccount()


def test_transfer_to_contract():
    # Deploy token
    token = DappToken.deploy({"from": account})
    # Deploy farm
    farm = TokenFarm.deploy(token.address, {"from": account})
    # Stake token to farm
    amount = 1 * 10 ** token.decimals()
    token.approve(farm.address, amount, {"from": account})
    farm.stakeTokens(amount, token.address, {"from": account})
    # Check token is in farm

    assert token.balanceOf(farm.address) == amount


def test_token_issuance():
    weth_amount = weth.balanceOf(account.address)
    dai_amount = dai.balanceOf(account.address)

    token = DappToken.deploy({"from": account})
    farm = TokenFarm.deploy(token.address, {"from": account})
    farm.addAllowedToken(
        config["networks"][network.show_active()]["weth"],
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    farm.addAllowedToken(
        config["networks"][network.show_active()]["dai"],
        config["networks"][network.show_active()]["dai_usd_price_feed"],
        {"from": account},
    )

    assert dai.balanceOf(farm.address) == dai_amount
    assert weth.balanceOf(farm.address) == weth_amount
