import streamlit as st
from modules import auth, akun, booking, rekap
from utils.db import init_db

# ======================
# CONFIG (WAJIB DI ATAS)
# ======================
st.set_page_config(
    page_title="Booking App",
    page_icon="📊",
    layout="wide"
)

# ======================
# INIT DB
# ======================
init_db()

# ======================
# DEBUG (optional)
# ======================
# st.write("APP RUNNING")

# ======================
# LOGIN CHECK
# ======================
if "user" not in st.session_state:
    auth.login()
    st.stop()

user = st.session_state.user

# ======================
# SIDEBAR
# ======================
st.sidebar.success(f"👤 {user['full_name']}")
st.sidebar.write(f"Role: {user['role']}")
st.sidebar.divider()

# ======================
# MENU
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
