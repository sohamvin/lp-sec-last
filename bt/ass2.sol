// SPDX-Liscence-Identifier: UNLISCENSED

pragma solidity ^0.8.0;

import "hardhat/console.sol";

contract StudentData{

    struct Student{
        uint256 PRN;
        uint256 roll;
        string name;
    }

    Student[] public arr;

    function addStudent(uint256 temp_PRN,  uint256 temp_roll, string memory temp_name) public  {
            for(uint i = 0; i < arr.length; i++){
                if(arr[i].PRN == temp_PRN)
                {
                    revert("THE STUDENT ALREADY EXSISTS");
                }
            }

            arr.push(Student(temp_PRN, temp_roll, temp_name));
    }

    function number_of_students() public view returns (uint256){
        return arr.length;
    }

    function display_all_students() public view {
        for(uint i = 0 ; i < arr.length ; i++)
        {
            console.log(arr[i].PRN);
            console.log(arr[i].roll);
            console.log(arr[i].name);
        }
    }

    function get_student_by_PRN(uint index) public view returns(Student memory){
        require(index < arr.length , "Invalid Index");
        return arr[index];
    }


}