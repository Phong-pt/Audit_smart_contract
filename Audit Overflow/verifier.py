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
