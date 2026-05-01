import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import get_connection


# ======================
# STYLE
# ======================
def load_style():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Quattrocento+Sans&display=swap" rel="stylesheet">

    <style>
    .stApp {
        background-color: #f5f5f5;
        font-family: 'Quattrocento Sans', Helvetica, Arial, sans-serif;
    }

    .stButton > button {
        background: black;
        color: white;
        border-radius: 10px;
        height: 42px;
        font-weight: 600;
    }

    div[data-testid="stContainer"] {
        padding: 20px;
        border-radius: 15px;
        background: white;
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)


# ======================
# MAIN
# ======================
def show():

    load_style()

    st.title("Dashboard Rekap")

    conn = get_connection()
    user = st.session_state.user

    # ======================
    # FILTER
    # ======================
    with st.container(border=True):

        st.subheader("Filter Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            start_date = st.date_input("Dari Tanggal")

        with col2:
            end_date = st.date_input("Sampai Tanggal")

        with col3:
            gender_filter = st.selectbox("Gender", ["ALL", "PRIA", "WANITA"])

    # ======================
    # QUERY
    # ======================
    if user["role"] == "admin":
        df = pd.read_sql("""
            SELECT 
                b.id,
                b.user_id,
                a.name_identity,
                a.group_id,
                a.type,
                a.gender,
                b.tanggal_booking,
                b.status
            FROM booking b
            JOIN akun_nusuk a ON b.akun_id = a.id
        """, conn)
    else:
        df = pd.read_sql("""
            SELECT 
                b.id,
                b.user_id,
                a.name_identity,
                a.group_id,
                a.type,
                a.gender,
                b.tanggal_booking,
                b.status
            FROM booking b
            JOIN akun_nusuk a ON b.akun_id = a.id
            WHERE b.user_id = ?
        """, conn, params=(user["id"],))

    if df.empty:
        st.warning("Belum ada data booking")
        return

    df["tanggal_booking"] = pd.to_datetime(df["tanggal_booking"])

    # ======================
    # FILTER DATA
    # ======================
    df = df[
        (df["tanggal_booking"].dt.date >= start_date) &
        (df["tanggal_booking"].dt.date <= end_date)
    ]

    if gender_filter != "ALL":
        df = df[df["gender"] == gender_filter]

    # ======================
    # METRICS
    # ======================
    with st.container(border=True):

        st.subheader("Summary")

        total_booking = len(df)
        total_group = df["group_id"].nunique()
        total_leader = len(df[df["type"] == "LEADER"])
        total_member = len(df[df["type"] == "MEMBER"])

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Booking", total_booking)
        col2.metric("Total Group", total_group)
        col3.metric("Leader", total_leader)
        col4.metric("Member", total_member)

    # ======================
    # CHART SEJAJAR
    # ======================
    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Booking per Hari")
            per_day = df.groupby(df["tanggal_booking"].dt.date).size()

            fig1, ax1 = plt.subplots()
            per_day.plot(ax=ax1)
            ax1.set_xlabel("Tanggal")
            ax1.set_ylabel("Jumlah")
            st.pyplot(fig1)

        with col2:
            st.subheader("Distribusi Gender")
            gender_count = df["gender"].value_counts()

            fig2, ax2 = plt.subplots()
            gender_count.plot(kind="bar", ax=ax2)
            st.pyplot(fig2)

    # ======================
    # TYPE CHART
    # ======================
    with st.container(border=True):

        st.subheader("Leader vs Member")

        type_count = df["type"].value_counts()

        fig3, ax3 = plt.subplots()
        type_count.plot(kind="bar", ax=ax3)
        st.pyplot(fig3)

    # ======================
    # REKAP TABLE SEJAJAR
    # ======================
    with st.container(border=True):

        col1, col2 = st.columns(2)

        if user["role"] == "admin":
            with col1:
                st.subheader("Rekap per User")

                user_summary = df.groupby("user_id").agg(
                    total_booking=("id", "count"),
                    total_group=("group_id", "nunique")
                ).reset_index()

                st.dataframe(user_summary, height=250)

        with col2:
            st.subheader("Rekap per Group")

            group_summary = df.groupby("group_id").agg(
                total_akun=("id", "count"),
                leader=("type", lambda x: (x == "LEADER").sum()),
                member=("type", lambda x: (x == "MEMBER").sum()),
            ).reset_index()

            st.dataframe(group_summary, height=250)

    # ======================
    # DETAIL TABLE
    # ======================
    with st.container(border=True):

        st.subheader("Detail Booking")

        st.dataframe(df, height=350)

        # EXPORT
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="rekap_booking.csv",
            mime="text/csv"
        )
