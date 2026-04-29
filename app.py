import streamlit as st
from utils.db import init_db
from modules import akun, booking, rekap
from login import show_login

# WAJIB PALING ATAS
st.set_page_config(page_title="NUSUK SYSTEM", layout="wide")

# INIT DB
init_db()

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# LOGIN
if st.session_state.user is None:
    show_login()
    st.stop()

# USER
user = st.session_state.user

# SIDEBAR
st.sidebar.write(f"👤 {user['full_name']}")
st.sidebar.caption(f"@{user['username']} | {user['role']}")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

menu = st.sidebar.selectbox("Menu", [
    "Akun Pria",
    "Akun Wanita",
    "Booking",
    "Rekapan"
])

# ROUTING
if menu == "Akun Pria":
    akun.show("PRIA")

elif menu == "Akun Wanita":
    akun.show("WANITA")

elif menu == "Booking":
    booking.show()

elif menu == "Rekapan":
    rekap.show()
