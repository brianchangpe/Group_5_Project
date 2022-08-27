pragma solidity ^0.5.0;

import "./complexCityToken.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";


contract ComplexCityTokenCrowdsale is Crowdsale, MintedCrowdsale{
    
    constructor(
        uint rate,
        address payable wallet,
        ComplexCityToken token
    )public
        Crowdsale(rate, wallet, token){}
}


contract ComplexCityTokenCrowdsaleDeployer {
    address public complexCity_token_address;
    address public complexCity_crowdsale_address;

    constructor(
        string memory name,
        string memory symbol,
        address payable wallet
    ) public {
        ComplexCityToken token = new ComplexCityToken(name, symbol, 0);
        complexCity_token_address = address(token);

        ComplexCityTokenCrowdsale complexCity_crowdsale = new ComplexCityTokenCrowdsale(1, wallet, token);
        complexCity_crowdsale_address = address(complexCity_crowdsale);

        token.addMinter(complexCity_crowdsale_address);
        token.renounceMinter();
    }
}