import streamlit as st

def show_login():

    # ======================
    # STYLE (WHITE MINIMAL)
    # ======================
    st.markdown("""
    <style>

    /* ===== BACKGROUND PUTIH ===== */
    .stApp {
        background-color: #ffffff;
    }

    /* ===== CENTER LAYOUT ===== */
    .block-container {
        padding-top: 6rem;
    }

    /* ===== BOX (CARD) ===== */
    div[data-testid="stContainer"] {
        background: #ffffff;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #eee;
    }

    /* ===== TITLE ===== */
    .title {
        text-align: center;
        font-size: 30px;
        font-weight: 600;
        color: #111;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }

    /* ===== INPUT ===== */
    .stTextInput input {
        background: #f9f9f9 !important;
        border: 1px solid #ddd !important;
        color: #111 !important;
        border-radius: 12px !important;
        padding: 12px;
    }

    .stTextInput label {
        color: #666 !important;
    }

    /* ===== CHECKBOX ===== */
    .stCheckbox label {
        color: #555 !important;
    }

    .stCheckbox input {
        accent-color: black !important;
    }

    /* ===== BUTTON ===== */
    .stButton>button {
        background: black;
        color: white;
        border-radius: 30px;
        height: 45px;
        font-weight: 600;
        border: none;
    }

    .stButton>button:hover {
        background: #333;
    }

    </style>
    """, unsafe_allow_html=True)

    # ======================
    # CENTER BOX
    # ======================
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.container(border=True):

            # TITLE
            st.markdown('<div class="title">User Login</div>', unsafe_allow_html=True)

            # INPUT
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            colA, colB = st.columns([1,1])

            with colA:
                remember = st.checkbox("Remember me")

            with colB:
                st.markdown(
                    "<p style='text-align:right;color:#888;'>Forgot?</p>",
                    unsafe_allow_html=True
                )

            # BUTTON
            if st.button("Login", use_container_width=True):

                USERS = {
                    "andy": {"id": 1, "password": "123", "role": "admin"},
                    "peri": {"id": 2, "password": "123", "role": "user"},
                    "arief": {"id": 3, "password": "123", "role": "user"},
                }

                if username in USERS and USERS[username]["password"] == password:
                    st.session_state.user = {
                        "id": USERS[username]["id"],
                        "username": username,
                        "role": USERS[username]["role"]
                    }
                    st.success("Login berhasil")
                    st.rerun()
                else:
                    st.error("Username / Password salah")
