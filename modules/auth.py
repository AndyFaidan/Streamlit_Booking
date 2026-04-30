import streamlit as st
from utils.db import get_connection
import hashlib

# ======================
# HASH PASSWORD
# ======================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ======================
# LOGIN
# ======================
def login():

    st.title("🔐 Login")

    conn = get_connection()

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):

        hashed = hash_password(password)

        user = conn.execute("""
            SELECT * FROM users
            WHERE username=? AND password=?
        """, (username, hashed)).fetchone()

        if user:
            st.session_state.user = {
                "id": user[0],
                "username": user[1],
                "full_name": user[3],
                "role": user[4]
            }
            st.success("Login berhasil ✅")
            st.rerun()
        else:
            st.error("Username / Password salah")


# ======================
# REGISTER
# ======================
def register():

    st.title("📝 Register")

    conn = get_connection()

    full_name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Register"):

        if not full_name or not username or not password:
            st.warning("Lengkapi semua field")
            return

        try:
            conn.execute("""
                INSERT INTO users (username, password, full_name, role)
                VALUES (?, ?, ?, ?)
            """, (
                username,
                hash_password(password),
                full_name,
                role
            ))
            conn.commit()

            st.success("Register berhasil ✅")
            st.info("Silakan login")

        except:
            st.error("Username sudah digunakan")