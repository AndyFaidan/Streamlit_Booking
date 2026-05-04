import streamlit as st
from streamlit_option_menu import option_menu
from modules import auth, akun, booking, rekap
from utils.db import init_db

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Booking App",
    page_icon="🖤",  # favicon hitam elegan
    layout="wide"
)

# ======================
# GLOBAL STYLE (ABU + HITAM)
# ======================
st.markdown("""
<style>

/* BACKGROUND UTAMA */
.stApp {
    background-color: #f5f5f5;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111111;
}

/* TEXT SIDEBAR */
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* CONTAINER CARD */
div[data-testid="stContainer"] {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
}

/* BUTTON */
.stButton > button {
    background-color: black;
    color: white;
    border-radius: 10px;
    height: 42px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #333;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ======================
# INIT DB
# ======================
init_db()

# ======================
# LOGIN
# ======================
if "user" not in st.session_state:
    auth.login()
    st.stop()

user = st.session_state.user

# ======================
# SIDEBAR MENU
# ======================
with st.sidebar:

    st.markdown(f"### 👤 {user['full_name']}")
    st.caption(f"Role: {user['role']}")
    st.divider()

    # ADMIN
    if user["role"] == "admin":
        selected = option_menu(
            menu_title=None,
            options=["Akun PRIA", "Akun WANITA", "Booking", "Rekap"],
            icons=["person", "person", "calendar-check", "bar-chart"],
            default_index=0,
            styles={
                "container": {
                    "background-color": "#111111",
                    "padding": "5px"
                },
                "icon": {
                    "color": "#bbbbbb",
                    "font-size": "18px"
                },
                "nav-link": {
                    "color": "#eeeeee",
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "4px",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "#e6e6e6",
                    "color": "black",
                    "font-weight": "bold",
                },
            }
        )

    # USER
    else:
        selected = option_menu(
            menu_title=None,
            options=["Booking", "Rekap"],
            icons=["calendar-check", "bar-chart"],
            default_index=0,
            styles={
                "container": {
                    "background-color": "#111111",
                    "padding": "5px"
                },
                "icon": {
                    "color": "#bbbbbb",
                    "font-size": "18px"
                },
                "nav-link": {
                    "color": "#eeeeee",
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "4px",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "#e6e6e6",
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
