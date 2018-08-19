pragma solidity ^0.4.0;

contract Test{

    constructor(string n, uint8 k) payable {
    }

    function getBalance() public {
        selfdestruct(msg.sender);
    }
}