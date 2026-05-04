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
# STYLE
# ======================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background-color: #e9e9e9;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #e9e9e9;
    padding: 15px;
}

/* CARD */
.card {
    background: #dcdcdc;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}

/* USER BOX */
.user-box {
    text-align: center;
    font-weight: 600;
    font-size: 18px;
}

/* SUBTEXT */
.user-role {
    font-size: 14px;
    color: #555;
}

/* TITLE */
.menu-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* LINE */
.divider {
    height: 1px;
    background: #bdbdbd;
    margin: 10px 0 20px 0;
}

/* OPTION MENU */
.nav-link {
    border-radius: 20px !important;
    padding: 12px !important;
    margin-bottom: 10px !important;
}

/* SELECTED */
.nav-link-selected {
    background-color: black !important;
    color: white !important;
    font-weight: 600;
}

/* ICON */
.nav-link i {
    color: black;
}

/* LOGOUT BUTTON */
.logout-btn button {
    background-color: black !important;
    color: white !important;
    border-radius: 20px !important;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
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
# SIDEBAR
# ======================
with st.sidebar:

    # USER CARD
    st.markdown(f"""
    <div class="card user-box">
        {user['full_name']}<br>
        <span class="user-role">{user['role']}</span>
    </div>
    """, unsafe_allow_html=True)

    # MENU CARD
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="menu-title">📺 Main Menu</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # MENU
    if user["role"] == "admin":
        selected = option_menu(
            menu_title=None,
            options=["Akun PRIA", "Akun WANITA", "Booking", "Rekap"],
            icons=["person", "person", "calendar-check", "bar-chart"],
            default_index=0,
            styles={
                "container": {"background-color": "transparent"},
                "nav-link": {"color": "black"},
                "nav-link-selected": {"background-color": "black"},
            }
        )
    else:
        selected = option_menu(
            menu_title=None,
            options=["Booking", "Rekap"],
            icons=["calendar-check", "bar-chart"],
            default_index=0,
            styles={
                "container": {"background-color": "transparent"},
                "nav-link": {"color": "black"},
                "nav-link-selected": {"background-color": "black"},
            }
        )

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
