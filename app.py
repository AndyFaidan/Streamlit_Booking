import streamlit as st
from streamlit_option_menu import option_menu
from modules import auth, akun, booking, rekap
from utils.db import init_db

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Booking App",
    page_icon="🖤",
    layout="wide"
)

# ======================
# GLOBAL STYLE
# ======================
st.markdown("""
<style>

/* ===== BACKGROUND UTAMA ===== */
.stApp {
    background-color: #f2f2f2;
}

/* ===== SIDEBAR GRADIENT ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #A6A6A6 0%,
        #8C8C8C 25%,
        #707070 50%,
        #545454 75%,
        #383838 100%
    );
}

/* ===== TEXT SIDEBAR ===== */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===== CARD CONTAINER ===== */
div[data-testid="stContainer"] {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
}

/* ===== BUTTON ===== */
.stButton > button {
    background-color: black;
    color: white;
    border-radius: 10px;
    height: 42px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #333;
}

/* ===== OPTION MENU CUSTOM ===== */
.nav-link {
    background-color: transparent !important;
    border-radius: 8px;
}

/* HOVER */
.nav-link:hover {
    background-color: rgba(255,255,255,0.1) !important;
}

/* SELECTED */
.nav-link-selected {
    background-color: white !important;
    color: black !important;
    font-weight: bold;
}

/* ICON */
.nav-link i {
    color: #e0e0e0;
}

/* ===== LOGOUT BUTTON ===== */
.stSidebar button {
    background-color: white;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}

.stSidebar button:hover {
    background-color: #d9d9d9;
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
# SIDEBAR MENU
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
                    "background-color": "transparent",
                },
                "icon": {
                    "color": "#e0e0e0",
                },
                "nav-link": {
                    "color": "white",
                    "margin": "4px",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "#ffffff",
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
                    "background-color": "transparent",
                },
                "icon": {
                    "color": "#e0e0e0",
                },
                "nav-link": {
                    "color": "white",
                    "margin": "4px",
                    "border-radius": "8px",
                },
                "nav-link-selected": {
                    "background-color": "#ffffff",
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
