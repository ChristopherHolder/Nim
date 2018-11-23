pragma solidity ^0.4.20;

contract Check {
    address owner = msg.sender;
    mapping(uint256 => bool) nonces;


    function Check() public payable { }

    function claim(uint256 amount,uint256 nonce,bytes32 msgHash,uint8 v,bytes32 r,bytes32 s) public {

        bytes32 hash = keccak256(msg.sender,amount,nonce,this);
        address ad1 = ecrecover(hash,v,r,s);
        address ad2 =  ecrecover(msgHash, v, r, s);
        require(ad1 == ad2);
        msg.sender.transfer(amount);

    }

    function kill() public {
        require(msg.sender == owner);
        selfdestruct(msg.sender);
    }

}