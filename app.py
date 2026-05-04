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
# INIT DB
# ======================
init_db()

# ======================
# STYLE GLOBAL
# ======================
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background-color: #f5f5f5;
    font-family: 'Quattrocento Sans', sans-serif;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #f5f5f5;
    padding: 15px;
}

/* ===== USER BOX ===== */
.user-box {
    padding: 15px;
    border-radius: 15px;
    background: #e9e9e9;
    text-align: center;
    margin-bottom: 20px;
    font-weight: 600;
}

/* ===== MENU CARD ===== */
.menu-card {
    background: #ffffff;
    padding: 15px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* ===== TITLE ===== */
.menu-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* ===== DIVIDER ===== */
.divider {
    height: 1px;
    background: #ddd;
    margin: 10px 0 15px 0;
}

/* ===== OPTION MENU ===== */
.nav-link {
    font-size: 15px;
    text-align: left;
    margin: 5px;
    padding: 10px;
    border-radius: 12px;
    color: black !important;
}

/* HOVER */
.nav-link:hover {
    background-color: #eeeeee !important;
}

/* SELECTED (HITAM FULL) */
.nav-link-selected {
    background-color: black !important;
    color: white !important;
    font-weight: 600;
    border-radius: 15px;
}

/* ICON DEFAULT */
.nav-link i {
    color: black;
}

/* ICON SELECTED */
.nav-link-selected i {
    color: white !important;
}

/* ===== LOGOUT BUTTON ===== */
.logout-btn button {
    background-color: black !important;
    color: white !important;
    border-radius: 20px !important;
    height: 48px;
    font-size: 15px;
    font-weight: 600;
}

.logout-btn button:hover {
    background-color: #333 !important;
}

</style>
""", unsafe_allow_html=True)

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
with st.sidebar:

    # USER BOX
    st.markdown(f"""
    <div class="user-box">
        {user['full_name']}<br>
        <small>{user['role']}</small>
    </div>
    """, unsafe_allow_html=True)

    # MENU CARD START
    st.markdown('<div class="menu-card">', unsafe_allow_html=True)

    st.markdown('<div class="menu-title">📺 Main Menu</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ======================
    # MENU ADMIN / USER
    # ======================
    if user["role"] == "admin":
        menu_list = ["Akun PRIA", "Akun WANITA", "Booking", "Rekap"]
        icons = ["person", "person-fill", "calendar-check", "bar-chart"]
    else:
        menu_list = ["Booking", "Rekap"]
        icons = ["calendar-check", "bar-chart"]

    selected = option_menu(
        menu_title=None,
        options=menu_list,
        icons=icons,
        default_index=0,
        styles={
            "container": {"background-color": "transparent"},
            "icon": {"color": "black", "font-size": "18px"},
            "nav-link": {"color": "black"},
            "nav-link-selected": {"background-color": "black"},
        }
    )

    # MENU CARD END
    st.markdown('</div>', unsafe_allow_html=True)

    # LOGOUT
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

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
