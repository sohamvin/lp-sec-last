// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.0;
contract Bank{

    uint256 balance = 0;
    address public accOwner;

    constructor(){
        accOwner = msg.sender;
    }

    function Deposit() public payable {
        require(accOwner == msg.sender , "Invalid Credentials");
        require(msg.value > 0 , "Invalid Value");
        balance = balance + msg.value;
    }

    function WithDraw()public payable {
        require(accOwner == msg.sender , "Invalid Credentials");
        require(msg.value > 0, "Invalid Value");
        require (msg.value <= balance , "Value Bounced");
        balance = balance - msg.value;
    }

    function ShowBalance()public view returns(uint256){
        require(accOwner == msg.sender , "Invalid Credentials");
        return balance;
    }

}