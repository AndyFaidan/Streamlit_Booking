
import streamlit as st
import pandas as pd
from utils.db import get_connection

def show():
    st.title("Rekapan")

    conn = get_connection()

    df = pd.read_sql("""
        SELECT a.email, a.gender, a.type, a.name_identity, b.qty, b.tanggal_booking, b.status
        FROM booking b
        JOIN akun_nusuk a ON b.akun_id = a.id
    """, conn)

    st.dataframe(df, use_container_width=True)
