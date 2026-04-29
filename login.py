import streamlit as st

def show_login():

    # ======================
    # PREMIUM UI CSS
    # ======================
    st.markdown("""
    <style>

    /* RESET */
    .block-container {
        padding: 0 !important;
    }

    /* BACKGROUND GRADIENT */
    .stApp {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }

    /* CENTER LAYOUT */
    .wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    /* CARD */
    .card {
        width: 380px;
        padding: 40px;
        border-radius: 20px;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: fadeIn 0.8s ease-in-out;
    }

    /* ANIMATION */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }

    /* TITLE */
    .title {
        text-align: center;
        font-size: 30px;
        font-weight: 600;
        color: white;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 14px;
        color: #ddd;
        margin-bottom: 30px;
    }

    /* INPUT */
    .stTextInput>div>div>input {
        border-radius: 12px;
        padding: 12px;
        border: none;
        background: rgba(255,255,255,0.9);
    }

    /* BUTTON */
    .stButton>button {
        width: 100%;
        padding: 12px;
        border-radius: 12px;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    /* FOOTER */
    .footer {
        text-align: center;
        margin-top: 20px;
        font-size: 12px;
        color: #ccc;
    }

    </style>
    """, unsafe_allow_html=True)

    # ======================
    # WRAPPER
    # ======================
    st.markdown('<div class="wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # ======================
    # HEADER
    # ======================
    st.markdown('<div class="title">NUSUK SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Login untuk melanjutkan</div>', unsafe_allow_html=True)

    # ======================
    # FORM
    # ======================
    username = st.text_input("Email / Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns([1,1])

    with col1:
        remember = st.checkbox("Remember me")

    with col2:
        st.markdown("<div style='text-align:right;font-size:12px;color:#ccc;'>Forgot?</div>", unsafe_allow_html=True)

    # ======================
    # LOGIN LOGIC
    # ======================
    if st.button("LOGIN"):

        users = {
            "andy": {"id": 1, "password": "123", "role": "admin"},
            "peri": {"id": 2, "password": "123", "role": "user"},
            "arief": {"id": 3, "password": "123", "role": "user"},
        }

        if username in users and users[username]["password"] == password:
            st.session_state.user = {
                "id": users[username]["id"],
                "username": username,
                "role": users[username]["role"]
            }
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username / Password salah")

    # ======================
    # FOOTER
    # ======================
    st.markdown('<div class="footer">© 2026 Nusuk System</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
