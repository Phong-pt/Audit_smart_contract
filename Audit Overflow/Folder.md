# Audit
Trước khi vào audit một smart contract , tôi muốn nói rằng bản quyền smart contract dưới đây thuộc về đội ngũ dreamhack. Bản thân tôi lấy smart contract của họ bởi tôi đã mua khóa học và đây là writeup cho các hợp đồng đầu tiên của bản thân. Vì đây là hợp đồng đầu tiên push lên và đây là challenge của dreamhack , sau này trước khi bắt đầu tôi sẽ luôn ghi lại nguồn của các hợp đồng thông minh được sử dụng để audit


## smart contract 
dưới đây là hợp đồng có chữa lỗi overflow/under flow. 
mọi người có thể đọc qua hợp đồng , tôi cũng đã comment từng dòng cho mọi người hiểu

Contract.sol

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Level {
    mapping(address => mapping(string => uint)) public inventory;
    // dau tien la gan ten gi do voi so luong, sau do gan dia chi vi cho ten va so luong trong inventory
    mapping(string => uint) public tokenCost;
    // gan ten vao so luong cua Gia tri token : vi du : Phong = 1000
    mapping(address => bool) public hasReceivedFreeMoney;
    // gan dia chi vao bool de kiem tra xem dia chi da nhan tien mien phi chua
    mapping(address => uint) public balance;
    // gan dia chi vao so du vi

    uint immutable fee;
    // khai vao mot bien khong the thay doi la fee

    constructor () public {
    // cac cau lenh duoi constructor se duoc thuc hien luon
        tokenCost["amo"] = 9254;
        tokenCost["boko"] = 6553;
        tokenCost["nando"] = 2178;
        // gan tokenCost cua amo = 9254, cua boko la 6553, nando = 2178

        fee = 0x10;
        // fee mac dinh la 0x10
    }

    function getFreeMoney() public returns (bool) { // ham getFreeMoney tra ve gia tri boolean
        if (hasReceivedFreeMoney[msg.sender]) // check xem dia chi vi cua nguoi goi hien tai 
            return false; // neu bang true thi tra nguoc ve false
        
        hasReceivedFreeMoney[msg.sender] = true; // mac dinh luc dau la true vi chua co tien
        balance[msg.sender] += 0x10000; // so du cua nguoi do se dc cong them 10000
        return true; // ham tra ve true
    }

    function checkOverflow(uint costPerItem, uint amount) private view {
    // ham check overflow dc truyen vao gia tri costPerItem, amount
        require(costPerItem != 0, "There is no such token");
        //require tao loi neu costperitem = 0 thi in ra dong kia
        require(amount != 0, "You need to buy at least one item");
				// tuong tu doi voi amount
        uint totalCost = costPerItem * amount;
        // cong thuc tinh tong : cosperitem * amount
        require(totalCost / amount == costPerItem, "No overflow in multiplication :(");
        // check lai
        require(balance[msg.sender] >= totalCost, "You do not have enough money :(");
        // check lai so du cua nguoi goi co = totalcost khong
    }

    function buyToken(string memory tokenName, uint amount) public {
	  // ham mua token dc truyen vao gia tri (ten token) luuw tam thoi) , so du
        uint costPerItem = tokenCost[tokenName];
        // khai bao costPerItem se = gia token, tren la goi ten token se ra gia token
        checkOverflow(costPerItem, amount);
        // kiem tra loi overflow

        balance[msg.sender] -= costPerItem * amount + fee;
        // khi nguoi mua thi so du se bi tru theo cong thuc ben canh
        inventory[msg.sender][tokenName] += amount;
        // inventoty cua nguoi do (o ten token ) se duoc cong theem so luong token vao
    }
}
```


dưới đây là verify.py

```python
  function checkOverflow(uint costPerItem, uint amount) private view {
    // ham check overflow dc truyen vao gia tri costPerItem, amount
        require(costPerItem != 0, "There is no such token");
        //require tao loi neu costperitem = 0 thi in ra dong kia
        require(amount != 0, "You need to buy at least one item");
				// tuong tu doi voi amount
        uint totalCost = costPerItem * amount;
        // cong thuc tinh tong : cosperitem * amount
        require(totalCost / amount == costPerItem, "No overflow in multiplication :(");
        // check lai
        require(balance[msg.sender] >= totalCost, "You do not have enough money :(");
        // check lai so du cua nguoi goi co = totalcost khong
    }
```

đọc nhanh file contract.sol thì chúng ta có thể thấy rằng 