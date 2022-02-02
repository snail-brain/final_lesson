from brownie import TokenFarm, network, config
from scripts.helpful_scripts import *

account = getAccount()


def main():
    farm = TokenFarm.deploy({"from": account})
    farm.addAllowedToken(
        config["networks"][network.show_active()]["weth"],
        config["networks"][network.show_active()]["eth_dai_price_feed"],
        {"from": account},
    )

    print(farm.getPrice(config["networks"][network.show_active()]["weth"]))


main()
