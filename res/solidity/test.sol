pragma solidity ^0.4.0;

contract Test{
    string d ;
    uint e;
    constructor(string s,uint256 n) payable {
        s = d;
        e = n;
    }
    function getBalance() public {
        selfdestruct(msg.sender);
    }
}