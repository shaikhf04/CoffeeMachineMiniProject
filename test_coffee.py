import pytest
from collections import defaultdict
from unittest.mock import MagicMock
import sys

# Mock streamlit before importing app
mock_st = MagicMock()
mock_st.session_state.instock = {"coffee": 10, "milk": 10, "water": 10, "sugar": 10}
mock_st.session_state.order_summary = defaultdict(int)
mock_st.session_state.total_bill = 0.0
mock_st.session_state.order_count = 0
mock_st.session_state.pending_item = None
mock_st.session_state.logs = []
mock_st.session_state.instock.items.return_value = [
    ("coffee", 10), ("milk", 10), ("water", 10), ("sugar", 10)
]
sys.modules["streamlit"] = mock_st

from app import check_stock, deduct_stock, confirm_payment, cancel_order, reset_machine, OutOfStockError

def test_check_stock_passes():
    check_stock("Black Coffee")

def test_check_stock_fails():
    mock_st.session_state.instock["coffee"] = 0
    with pytest.raises(OutOfStockError):
        check_stock("Black Coffee")

def test_deduct_stock():
    mock_st.session_state.instock = {"coffee": 10, "milk": 10, "water": 10, "sugar": 10}
    deduct_stock("Latte")
    assert mock_st.session_state.instock["coffee"] == 9

def test_confirm_payment():
    mock_st.session_state.total_bill = 0.0
    confirm_payment("Black Coffee")
    assert mock_st.session_state.total_bill == 10.0

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
