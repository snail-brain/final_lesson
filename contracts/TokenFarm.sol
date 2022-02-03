// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    address[] public allowedTokens;
    mapping(address => AggregatorV3Interface) public price_feeds;
    address public DappToken;

    address[] public stakers;
    mapping(address => mapping(address => uint256)) public balances;
    mapping(address => uint256) public uniqueTokensStaked;

    constructor(address _dappTokenAddress) public {
        DappToken = _dappTokenAddress;
    }

    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "You don't have any tokens to deposit!");
        require(tokenIsAllowed(_token), "Token not supported!");

        IERC20(_token).transferFrom(msg.sender, address(this), _amount);

        if (uniqueTokensStaked[msg.sender] < 1) {
            stakers.push((msg.sender));
        }
        updateUniqueTokensStaked(msg.sender, _token);
        balances[msg.sender][_token] += _amount;
    }

    function issueTokens() public onlyOwner {
        for (uint256 i = 0; i < stakers.length; i++) {
            address staker = stakers[i];
            uint256 userTVL = findUserTVL(staker);
            uint256 amountToTransfer;

            IERC20(DappToken).transfer(staker, amountToTransfer);
        }
    }

    function findUserTVL(address _staker) public view returns (uint256) {
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_staker] > 0, "No tokens staked!");
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            totalValue += getUserSingleTokenValue(_staker, allowedTokens[i]);
        }
        return totalValue;
    }

    function getUserSingleTokenValue(address _staker, address _token)
        internal
        view
        returns (uint256)
    {
        (uint256 price, uint256 decimals) = getTokenValue(_token);
        uint256 amountStaked = balances[_staker][_token];

        return (amountStaked * price) / (10**decimals);
    }

    function getTokenValue(address _token)
        internal
        view
        returns (uint256, uint256)
    {
        (, int256 price, , , ) = price_feeds[_token].latestRoundData();
        return (uint256(price), uint256(price_feeds[_token].decimals()));
    }

    function updateUniqueTokensStaked(address _user, address _token) internal {
        if (balances[_user][_token] <= 0) {
            uniqueTokensStaked[_user] += 1;
        }
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            if (allowedTokens[i] == _token) {
                return true;
            }
        }
        return false;
    }

    function addAllowedToken(address _token, address _price_feed)
        public
        onlyOwner
    {
        allowedTokens.push(_token);
        price_feeds[_token] = AggregatorV3Interface(_price_feed);
    }
}
