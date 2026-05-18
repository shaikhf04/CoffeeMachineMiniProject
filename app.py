import streamlit as st
from collections import defaultdict

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Coffee Bot ☕", page_icon="☕", layout="centered")

# ── Custom Exception ──────────────────────────────────────────────────────────
class OutOfStockError(Exception):
    pass

# ── Data (from data/menu.py) ──────────────────────────────────────────────────
item = ["Black Coffee", "Latte", "Cappuccino"]

bill = {"Black Coffee": 10, "Latte": 15, "Cappuccino": 20}

blackCoffee  = {"coffee": 1, "milk": 0, "water": 1, "sugar": 0}
latte        = {"coffee": 1, "milk": 1, "water": 1, "sugar": 1}
cappuccino   = {"coffee": 1, "milk": 2, "water": 1, "sugar": 0}

recipes = {
    "Black Coffee": blackCoffee,
    "Latte":        latte,
    "Cappuccino":   cappuccino,
}

# ── Session state (replaces global variables) ─────────────────────────────────
if "instock" not in st.session_state:
    st.session_state.instock = {"coffee": 10, "milk": 10, "water": 10, "sugar": 10}

if "order_summary" not in st.session_state:
    st.session_state.order_summary = defaultdict(int)

if "total_bill" not in st.session_state:
    st.session_state.total_bill = 0.0

if "order_count" not in st.session_state:
    st.session_state.order_count = 0

if "pending_item" not in st.session_state:
    st.session_state.pending_item = None   # item waiting for payment confirm

if "logs" not in st.session_state:
    st.session_state.logs = []

# ── Helper functions ──────────────────────────────────────────────────────────
def log(msg):
    st.session_state.logs.append(msg)

def check_stock(menu_item):
    recipe = recipes[menu_item]
    for ingredient, needed in recipe.items():
        if needed == 0:
            continue
        available = st.session_state.instock.get(ingredient, 0)
        log(f"{ingredient}: need {needed}, in stock {available}")
        if needed > available:
            raise OutOfStockError(f"Not enough {ingredient} to make {menu_item}.")

def deduct_stock(menu_item):
    recipe = recipes[menu_item]
    for ingredient, needed in recipe.items():
        st.session_state.instock[ingredient] -= needed
    log(f"Stock updated after making {menu_item}")

def confirm_payment(menu_item):
    st.session_state.total_bill += bill[menu_item]
    st.session_state.order_summary[menu_item] += 1
    st.session_state.order_count += 1
    st.session_state.pending_item = None
    log(f"Payment confirmed for {menu_item}. Total so far: ${st.session_state.total_bill:.2f}")

def cancel_order():
    st.session_state.pending_item = None
    log("Order cancelled by user.")

def reset_machine():
    st.session_state.instock        = {"coffee": 10, "milk": 10, "water": 10, "sugar": 10}
    st.session_state.order_summary  = defaultdict(int)
    st.session_state.total_bill     = 0.0
    st.session_state.order_count    = 0
    st.session_state.pending_item   = None
    st.session_state.logs           = []

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }
        h1, h2, h3 {
            font-family: 'Playfair Display', serif !important;
        }
        .coffee-card {
            background: #1c1008;
            border: 1px solid #4a2c0a;
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 12px;
            color: #f5e6c8;
        }
        .stock-badge {
            background: #2e1a06;
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 0.85rem;
            color: #d4a96a;
            display: inline-block;
            margin: 3px;
        }
        .stButton > button {
            background-color: #6b3a1f;
            color: #f5e6c8;
            border: none;
            border-radius: 10px;
            font-family: 'DM Sans', sans-serif;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #8b5a2b;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.title("☕ Coffee Bot")
st.caption("Your virtual barista — order, pay, enjoy.")

st.divider()

# ── Stock display ─────────────────────────────────────────────────────────────
with st.expander("🧂 Current Stock", expanded=False):
    cols = st.columns(4)
    for i, (ingredient, qty) in enumerate(st.session_state.instock.items()):
        cols[i].metric(ingredient.capitalize(), qty)

st.divider()

# ── Payment confirmation screen ───────────────────────────────────────────────
if st.session_state.pending_item:
    pending = st.session_state.pending_item
    st.subheader("💳 Confirm Payment")
    st.markdown(f"""
    <div class="coffee-card">
        <b>Item:</b> {pending}<br>
        <b>Amount:</b> ${bill[pending]:.2f}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, Pay Now", use_container_width=True):
            confirm_payment(pending)
            st.success(f"Payment confirmed! Your {pending} is being prepared ☕")
            st.rerun()
    with col2:
        if st.button("❌ Cancel Order", use_container_width=True):
            cancel_order()
            st.warning("Order cancelled.")
            st.rerun()

# ── Main menu ─────────────────────────────────────────────────────────────────
else:
    st.subheader("📋 Menu")
    for coffee_item in item:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{coffee_item}**")
        with col2:
            st.markdown(f"${bill[coffee_item]:.2f}")
        with col3:
            if st.button("Order", key=coffee_item, use_container_width=True):
                try:
                    check_stock(coffee_item)
                    deduct_stock(coffee_item)
                    st.session_state.pending_item = coffee_item
                    st.rerun()
                except OutOfStockError as e:
                    st.error(str(e))
                    log(f"Order failed: {e}")

# ── Order summary ─────────────────────────────────────────────────────────────
if st.session_state.order_count > 0:
    st.divider()
    st.subheader("🧾 Order Summary")
    for ordered_item, qty in st.session_state.order_summary.items():
        st.markdown(f"- {ordered_item}: {qty} x ${bill[ordered_item]} = **${qty * bill[ordered_item]}**")
    st.markdown(f"**Total Items:** {st.session_state.order_count}")
    st.markdown(f"### 💰 Total Bill: ${st.session_state.total_bill:.2f}")

# ── Reset button ──────────────────────────────────────────────────────────────
st.divider()
if st.button("🔄 Reset Machine", use_container_width=True):
    reset_machine()
    st.rerun()

# ── Logs ──────────────────────────────────────────────────────────────────────
if st.session_state.logs:
    with st.expander("📝 Activity Log", expanded=False):
        for entry in st.session_state.logs:
            st.text(entry)
