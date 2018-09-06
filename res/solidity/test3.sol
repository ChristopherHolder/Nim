pragma solidity ^0.4.0;

contract Test{

    event Address(address ad);
    constructor() public {
    }
    function hash(uint256 n) public returns (bytes32){
        return keccak256(n);
    }

    function hash2(uint256 amount, uint256 nonce) public returns(bytes32){
        return keccak256(msg.sender,amount,nonce,this);
    }
    function hash3() public {
        Address(msg.sender);
    }
}