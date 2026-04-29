import streamlit as st

# WAJIB PALING ATAS (JANGAN ADA CODE SEBELUM INI)
st.set_page_config(page_title="NUSUK SYSTEM", layout="wide")

# ======================
# IMPORT MODULE
# ======================
from utils.db import init_db
from modules import akun, booking, rekap
from login import show_login

# ======================
# INIT DATABASE
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
# USER INFO
# ======================
user = st.session_state.user

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.markdown("### 👤 User Info")
    st.write(f"**{user['full_name']}**")
    st.caption(f"@{user['username']} | {user['role']}")

    st.divider()

    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.rerun()

    st.divider()

    menu = st.selectbox("📌 Menu", [
        "Akun Pria",
        "Akun Wanita",
        "Booking",
        "Rekapan"
    ])

# ======================
# MAIN HEADER
# ======================
st.title("📊 NUSUK MANAGEMENT SYSTEM")

# ======================
# ROUTING
# ======================
try:
    if menu == "Akun Pria":
        akun.show("PRIA")

    elif menu == "Akun Wanita":
        akun.show("WANITA")

    elif menu == "Booking":
        booking.show()

    elif menu == "Rekapan":
        rekap.show()

except Exception as e:
    st.error("Terjadi error di module")
    st.exception(e)
