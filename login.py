import streamlit as st

# ======================
# USER DATA
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
# LOGIN FUNCTION
# ======================
def show_login():

    st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .block-container { padding-top: 6rem; }

    div[data-testid="stContainer"] {
        background: #ffffff;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #eee;
    }

    .title {
        text-align: center;
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 25px;
    }

    .stButton>button {
        background: black;
        color: white;
        border-radius: 25px;
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        with st.container(border=True):

            st.markdown('<div class="title">User Login</div>', unsafe_allow_html=True)

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            st.checkbox("Remember me")

            if st.button("Login", use_container_width=True):

                if username in USERS and USERS[username]["password"] == password:

                    st.session_state.user = {
                        "id": USERS[username]["id"],
                        "username": username,
                        "role": USERS[username]["role"],
                        "full_name": USERS[username]["full_name"]
                    }

                    st.success(f"Welcome, {USERS[username]['full_name']}")
                    st.rerun()

                else:
                    st.error("Username / Password salah")
