import streamlit as st
import os

USERS = {
    "andy": {
        "id": 1,
        "password": "123",
        "full_name": "Andy Sofyan Guspriyanto",
        "role": "admin"
    }
}
{
    "Zedd": {
        "id": 2,
        "password": "1933",
        "full_name": "Peri Romadon",
        "role": "admin"
    }
}
{
    "Ariefksf": {
        "id": 1,
        "password": "123",
        "full_name": "Arief Zaenal Hakim",
        "role": "admin"
    }
}

def login():

    # ======================
    # STYLE
    # ======================
    st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
    }

    .title {
        text-align: center;
        font-size: 26px;
        font-weight: 600;
        margin-top: 20px;
    }

    .stTextInput > div > div > input {
        border: 0.5px solid black;   /* hanya garis kotak */
        border-radius: 10px;
    }

    .stButton > button {
        background: black;
        color: white;
        border-radius: 10px;
        height: 45px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    # ======================
    # CENTER PAGE
    # ======================
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        with st.container(border=True):

            # ======================
            # LOGO CENTER FIX
            # ======================
            c1, c2, c3 = st.columns([1,2,1])

            with c2:
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                image_path = os.path.join(BASE_DIR, "images", "medina-removebg-preview.png" )

                st.image(image_path, width=1600)

            # ======================
            # TITLE
            # ======================
            st.markdown('<div class="title">Sign in</div>', unsafe_allow_html=True)
           

            # ======================
            # INPUT
            # ======================
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            # ======================
            # REMEMBER
            # ======================
            remember = st.checkbox("Remember me")

            # ======================
            # BUTTON
            # ======================
            if st.button("Continue", use_container_width=True):

                if username in USERS and USERS[username]["password"] == password:

                    user = USERS[username]

                    st.session_state.user = {
                        "id": user["id"],
                        "username": username,
                        "full_name": user["full_name"],
                        "role": user["role"]
                    }

                    st.session_state.remember = remember

                    st.success(f"Welcome, {user['full_name']} ✅")
                    st.rerun()

                else:
                    st.error("Username / Password salah")
