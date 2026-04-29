import streamlit as st

USERS = {
    "andy": {"id": 1, "password": "123", "role": "admin"},
    "peri": {"id": 2, "password": "123", "role": "user"},
    "arief": {"id": 3, "password": "123", "role": "user"},
}

def show_login():

    st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    .block-container { padding-top: 6rem; }

    div[data-testid="stContainer"] {
        border-radius: 20px;
        padding: 40px;
        border: 1px solid #eee;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }

    .title {
        text-align:center;
        font-size:30px;
        font-weight:600;
        margin-bottom:30px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        with st.container(border=True):

            st.markdown('<div class="title">User Login</div>', unsafe_allow_html=True)

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login", use_container_width=True):

                if username in USERS and USERS[username]["password"] == password:
                    st.session_state.user = {
                        "id": USERS[username]["id"],
                        "username": username,
                        "role": USERS[username]["role"]
                    }
                    st.success("Login berhasil")
                    st.rerun()
                else:
                    st.error("Login gagal")
