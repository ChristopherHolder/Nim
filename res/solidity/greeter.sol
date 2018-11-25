pragma solidity ^0.4.0;
//
contract Greeter {
    string public greeting;

    function Greeter(string k) payable {
        greeting = k;
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}