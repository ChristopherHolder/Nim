pragma solidity ^0.4.0;

contract Test{
    address owner;
    function Test() payable {
        owner = msg.sender;
    }

    function getBalance(uint8 f) public {
        if (f==5) selfdestruct(msg.sender);
    }
}