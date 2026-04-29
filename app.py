import streamlit as st
from utils.db import init_db
from modules import akun, booking, rekap

st.set_page_config(page_title="NUSUK SYSTEM", layout="wide")

# ======================
# INIT DB
# ======================
init_db()

# ======================
# USER CONFIG
# ======================
USERS = {
    "andy": {
        "id": 1,
        "password": "123",
        "role": "admin",
        "full_name": "Andy Sofyan Guspriyanto"
    },
    "peri": {
        "id": 2,
        "password": "123",
        "role": "user",
        "full_name": "Peri Romadon"
    },
    "arief": {
        "id": 3,
        "password": "123",
        "role": "user",
        "full_name": "Arief Zaenal Hakim"
    },
}

# ======================
# LOGIN STATE
# ======================
if "user" not in st.session_state:
    st.session_state.user = None

# ======================
# LOGIN PAGE
# ======================
if st.session_state.user is None:

    st.title("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.user = {
                "id": USERS[username]["id"],
                "username": username,
                "role": USERS[username]["role"],
                "full_name": USERS[username]["full_name"]
            }
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username / Password salah")

    st.stop()

# ======================
# USER INFO
# ======================
user = st.session_state.user

st.sidebar.write(f"👤 {user['full_name']}")
st.sidebar.caption(f"@{user['username']} | {user['role']}")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# ======================
# MENU
# ======================
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
