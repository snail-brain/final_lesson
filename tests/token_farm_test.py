from scripts.helpful_scripts import *
from brownie import TokenFarm, DappToken, config, network

account = getAccount()


def test_transfer_to_contract():
    # Deploy token
    token = DappToken.deploy({"from": account})
    # Deploy farm
    farm = TokenFarm.deploy([token.address], {"from": account})
    # Stake token to farm
    amount = 1 * 10 ** token.decimals()
    token.approve(farm.address, amount, {"from": account})
    farm.stakeTokens(amount, token.address, {"from": account})
    # Check token is in farm
    assert token.balanceOf(farm.address) == amount


def test_token_issuance():
    token = DappToken.deploy({"from": account})
    farm = TokenFarm.deploy([token.address], {"from": account})
    farm.addAllowedToken(
        config["networks"][network.show_active()]["weth"],
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
