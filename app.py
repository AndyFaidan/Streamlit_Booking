import streamlit as st

# ======================
# IMPORT MODULE
# ======================
from modules import auth, akun, booking, rekap
from utils.db import init_db

# ======================
# INIT DATABASE
# ======================
init_db()

# ======================
# CONFIG PAGE
# ======================
st.set_page_config(
    page_title="Booking App",
    page_icon="📊",
    layout="wide"
)

# ======================
# BELUM LOGIN
# ======================
if "user" not in st.session_state:

    st.sidebar.title("🔐 Authentication")

    menu = st.sidebar.radio("Menu", ["Login", "Register"])

    if menu == "Login":
        auth.login()
    else:
        auth.register()

    st.stop()

# ======================
# SUDAH LOGIN
# ======================
user = st.session_state.user

# ======================
# SIDEBAR USER INFO
# ======================
st.sidebar.success(f"👤 {user['full_name']}")
st.sidebar.write(f"Role: {user['role']}")

st.sidebar.divider()

# ======================
# MENU (ROLE BASED)
# ======================
if user["role"] == "admin":
    menu = st.sidebar.radio("Menu", [
        "Akun PRIA",
        "Akun WANITA",
        "Booking",
        "Rekap"
    ])
else:
    menu = st.sidebar.radio("Menu", [
        "Booking",
        "Rekap"
    ])

# ======================
# ROUTING
# ======================
if menu == "Akun PRIA":
    akun.show("PRIA")

elif menu == "Akun WANITA":
    akun.show("WANITA")

elif menu == "Booking":
    booking.show()

elif menu == "Rekap":
    rekap.show()

# ======================
# LOGOUT
# ======================
st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()
