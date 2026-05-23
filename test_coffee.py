def test_bill_calculation():
    bill = {"Black Coffee": 10, "Latte": 15, "Cappuccino": 20}
    assert bill["Black Coffee"] == 10
    assert bill["Latte"] == 15
    assert bill["Cappuccino"] == 20
