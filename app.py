import streamlit as st
from login import show_login
from utils.db import init_db
from modules import akun, booking, rekap

# HARUS PALING ATAS
st.set_page_config(page_title="NUSUK SYSTEM")

init_db()

# ======================
# LOGIN CHECK
# ======================
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    show_login()
    st.stop()

# ======================
# SIDEBAR
# ======================
user = st.session_state.user

st.sidebar.write(f"Login: **{user['username']}**")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

menu = st.sidebar.selectbox("Menu", [
    "Akun Pria",
    "Akun Wanita",
    "Booking",
    "Rekapan"
])

# ======================
# ROUTING
# ======================
if menu == "Akun Pria":
    akun.show("PRIA")

elif menu == "Akun Wanita":
    akun.show("WANITA")

elif menu == "Booking":
    booking.show()

elif menu == "Rekapan":
    rekap.show()
