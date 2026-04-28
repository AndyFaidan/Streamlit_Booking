
import streamlit as st
from utils.db import init_db
from modules import akun, booking, rekap

st.set_page_config(page_title="NUSUK SYSTEM (Single DB)", layout="wide")

# init DB
init_db()

# simple session user (optional)
if "user" not in st.session_state:
    st.session_state.user = {"id": 1, "username": "default"}

st.sidebar.title("Menu")

menu = st.sidebar.selectbox("Pilih Menu", [
    "Akun Pria",
    "Akun Wanita",
    "Booking",
    "Rekapan"
])

if menu == "Akun Pria":
    akun.show("PRIA")
elif menu == "Akun Wanita":
    akun.show("WANITA")
elif menu == "Booking":
    booking.show()
elif menu == "Rekapan":
    rekap.show()
