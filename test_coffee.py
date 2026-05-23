def test_bill_calculation():
    bill = {"Black Coffee": 10, "Latte": 15, "Cappuccino": 20}
    assert bill["Black Coffee"] == 10
    assert bill["Latte"] == 15
    assert bill["Cappuccino"] == 20    assert mock_st.session_state.total_bill == 10.0

def test_cancel_order():
    mock_st.session_state.pending_item = "Latte"
    cancel_order()
    assert mock_st.session_state.pending_item is None

def test_reset_machine():
    mock_st.session_state.total_bill = 99.0
    mock_st.session_state.order_count = 5
    reset_machine()
    assert mock_st.session_state.total_bill == 0.0
    assert mock_st.session_state.order_count == 0
    assert mock_st.session_state.instock == {"coffee": 10, "milk": 10, "water": 10, "sugar": 10}
