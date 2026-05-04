import streamlit as st
from streamlit_option_menu import option_menu
from modules import auth, akun, booking, rekap
from utils.db import init_db

# ======================
# CONFIG (WAJIB PALING ATAS)
# ======================
st.set_page_config(
    page_title="Booking App",
    page_icon="📊",
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
.stApp {
    background-color: #f5f5f5;
    font-family: 'Quattrocento Sans', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
}

/* Hilangkan garis atas */
section[data-testid="stSidebar"] hr {
    margin-top: 10px;
}

/* User info */
.user-box {
    padding: 10px;
    border-radius: 10px;
    background: #f1f1f1;
    text-align: center;
    margin-bottom: 15px;
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

    st.markdown(f"""
    <div class="user-box">
        <b>{user['full_name']}</b><br>
    </div>
    """, unsafe_allow_html=True)

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
        "Main Menu",
        menu_list,
        icons=icons,
        menu_icon="cast",
        default_index=0,

        # ======================
        # STYLE MENU (HITAM)
        # ======================
        styles={
            "container": {
                "padding": "5px",
                "background-color": "#ffffff",
            },

            "icon": {
                "color": "black",
                "font-size": "18px"
            },

            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "5px",
                "padding": "10px",
                "--hover-color": "#eeeeee",
                "color": "black",
                "border-radius": "10px",
            },

            # 🔥 SELECTED HITAM
            "nav-link-selected": {
                "background-color": "#000000",
                "color": "white",
                "font-weight": "600",
                "border-radius": "12px",
            },

            "menu-title": {
                "font-size": "20px",
                "font-weight": "600",
                "color": "black"
            }
        }
    )

    st.divider()

    if st.button("LogOut", use_container_width=True):
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
