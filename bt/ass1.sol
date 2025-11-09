// SPDX-License-Identifier: MIT
pragma solidity ^0.8.29;
contract BankAccount {

    mapping(address => uint256) private balances;

    event Deposit(address indexed customer, uint256 amount, uint256 newBal);
    event Withdrawal(address indexed  customer, uint256 amount, uint newBalance);

    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");
        
        // Add the deposited amount to the caller's balance
        balances[msg.sender] += msg.value;
        
        // Emit an event to record this deposit on the blockchain
        emit Deposit(msg.sender, msg.value, balances[msg.sender]);
    }

        function withdraw(uint256 amount) public {
        // First, check if the caller has enough balance
        require(amount > 0, "Withdrawal amount must be greater than zero");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Subtract the amount from the caller's balance BEFORE sending
        // This is important for security (prevents re-entrancy attacks)
        balances[msg.sender] -= amount;
        
        // Transfer the ETH to the caller
        // payable() converts the address to one that can receive ETH
        payable(msg.sender).transfer(amount);
        
        // Emit an event to record this withdrawal
        emit Withdrawal(msg.sender, amount, balances[msg.sender]);
    }

        function showBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
    
    // Optional: Function to check any address's balance (useful for testing)
    function getBalance(address customer) public view returns (uint256) {
        return balances[customer];
    }
    
}


