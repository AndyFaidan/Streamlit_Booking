import streamlit as st

# ======================
# USER DATA (SINGLE SOURCE)
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

def show_login():

    # ======================
    # STYLE (WHITE MINIMAL)
    # ======================
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
        font-size: 30px;
        font-weight: 600;
        color: #111;
        margin-bottom: 30px;
    }

    .stTextInput input {
        background: #f9f9f9 !important;
        border: 1px solid #ddd !important;
        color: #111 !important;
        border-radius: 12px !important;
        padding: 12px;
    }

    .stCheckbox label { color: #555 !important; }
    .stCheckbox input { accent-color: black !important; }

    .stButton>button {
        background: black;
        color: white;
        border-radius: 30px;
        height: 45px;
        font-weight: 600;
        border: none;
    }

    .stButton>button:hover { background: #333; }
    </style>
    """, unsafe_allow_html=True)

    # ======================
    # CENTER BOX
    # ======================
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.container(border=True):

            st.markdown('<div class="title">User Login</div>', unsafe_allow_html=True)

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            colA, colB = st.columns(2)

            with colA:
                st.checkbox("Remember me")

            with colB:
                st.markdown(
                    "<p style='text-align:right;color:#888;'>Forgot?</p>",
                    unsafe_allow_html=True
                )

            # ======================
            # LOGIN ACTION
            # ======================
            if st.button("Login", use_container_width=True):

                if username in USERS and USERS[username]["password"] == password:

                    st.session_state.user = {
                        "id": USERS[username]["id"],
                        "username": username,
                        "role": USERS[username]["role"],
                        "full_name": USERS[username]["full_name"]
                    }

                    st.success(f"Welcome, {USERS[username]['full_name']} 👋")
                    st.rerun()

                else:
                    st.error("Username / Password salah")ss
