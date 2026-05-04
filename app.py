import streamlit as st
from streamlit_option_menu import option_menu
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
# STYLE SIDEBAR HITAM
# ======================
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #000000;
}
</style>
""", unsafe_allow_html=True)

# ======================
# INIT DB
# ======================
init_db()

# ======================
# LOGIN CHECK
# ======================
if "user" not in st.session_state:
    auth.login()
    st.stop()

user = st.session_state.user

# ======================
# SIDEBAR + OPTION MENU
# ======================
with st.sidebar:

    st.markdown(f"### 👤 {user['full_name']}")
    st.caption(f"Role: {user['role']}")
    st.divider()

    # ADMIN MENU
    if user["role"] == "admin":
        selected = option_menu(
            menu_title=None,
            options=["Akun PRIA", "Akun WANITA", "Booking", "Rekap"],
            icons=["person", "person", "calendar-check", "bar-chart"],
            default_index=0,
            styles={
                "container": {
                    "background-color": "#000000",
                    "padding": "5px"
                },
                "icon": {
                    "color": "white",
                    "font-size": "18px"
                },
                "nav-link": {
                    "color": "white",
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "5px",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "white",
                    "color": "black",
                    "font-weight": "bold",
                },
            }
        )

    # USER MENU
    else:
        selected = option_menu(
            menu_title=None,
            options=["Booking", "Rekap"],
            icons=["calendar-check", "bar-chart"],
            default_index=0,
            styles={
                "container": {
                    "background-color": "#000000",
                    "padding": "5px"
                },
                "icon": {
                    "color": "white",
                    "font-size": "18px"
                },
                "nav-link": {
                    "color": "white",
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "5px",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "white",
                    "color": "black",
                    "font-weight": "bold",
                },
            }
        )

    st.divider()

    # LOGOUT
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ======================
# ROUTING
# ======================
if selected == "Akun PRIA":
    akun.show("PRIA")

elif selected == "Akun WANITA":
    akun.show("WANITA")

elif selected == "Booking":
    booking.show()

elif selected == "Rekap":
    rekap.show()
