pragma solidity ^0.4.0;

contract Test{

    event Address(address ad);
    event Hash(bytes32 by);
    constructor() public {
    }
    function hash(uint256 n) public returns (bytes32){
        return keccak256(n);
    }

    function hashSpecial(uint256 amount, uint256 nonce) public {
        emit Hash(keccak256(msg.sender,amount,nonce,this));
    }
    function returnAddress() public {
        emit Address(msg.sender);
    }
    function hashSenderAddress() public{
        emit Hash(keccak256(msg.sender));
    }
}