import streamlit as st
from utils.db import init_db
from modules import akun, booking, rekap
from login import show_login

# ======================
# CONFIG (WAJIB PALING ATAS)
# ======================
st.set_page_config(page_title="NUSUK SYSTEM", layout="centered")

# ======================
# INIT DB
# ======================
init_db()

# ======================
# INIT SESSION
# ======================
if "user" not in st.session_state:
    st.session_state.user = None

# ======================
# LOGIN PAGE
# ======================
if st.session_state.user is None:
    show_login()
    st.stop()

# ======================
# USER DATA
# ======================
user = st.session_state.user

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.markdown(f"### 👤 {user['full_name']}")
    st.caption(f"@{user['username']} | {user['role']}")

    st.divider()

    if st.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.rerun()

    st.divider()

    menu = st.selectbox("Menu", [
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
