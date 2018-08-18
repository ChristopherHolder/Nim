pragma solidity ^0.4.0;

contract Check{
    address deployer;

    mapping(uint8 => bool) ids;

    constructor(string n, uint8 k) payable {
        deployer = msg.sender;
    }

    function getBalance() public {
        selfdestruct(msg.sender);
    }
}