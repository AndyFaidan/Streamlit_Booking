import streamlit as st
import pandas as pd
from utils.db import get_connection
from datetime import datetime

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

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px;
        border: 1px solid #ccc;
        height: 42px;
    }

    .stButton > button {
        background: black;
        color: white;
        border-radius: 10px;
        height: 42px;
        font-weight: 600;
    }

    div[data-testid="stContainer"] {
        padding: 25px;
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

    st.title("Booking")

    conn = get_connection()
    user = st.session_state.user

    # ======================
    # FORM BOOKING
    # ======================
    with st.container(border=True):

        st.subheader("Form Booking")

        gender = st.selectbox("Pilih Gender", ["PRIA", "WANITA"])

        akun = pd.read_sql("""
            SELECT * FROM akun_nusuk
            WHERE user_id=? 
            AND status='READY'
            AND gender=?
        """, conn, params=(user["id"], gender))

        if akun.empty:
            st.warning(f"Tidak ada akun READY untuk {gender}")

        else:
            akun_map = {
                f"{r['name_identity']} | {r['email']} (G{r['group_id']})": r["id"]
                for _, r in akun.iterrows()
            }

            selected = st.selectbox("Pilih Akun", list(akun_map.keys()))
            akun_id = akun_map[selected]

            col1, col2 = st.columns(2)

            with col1:
                tgl = st.date_input("Tanggal")

            with col2:
                jam = st.time_input("Jam")

            if st.button("Booking", use_container_width=True):

                conn.execute("""
                    INSERT INTO booking
                    (user_id, akun_id, gender, tanggal_booking, qty, status)
                    VALUES (?,?,?,?,?,?)
                """, (
                    user["id"],
                    akun_id,
                    gender,
                    datetime.combine(tgl, jam),
                    1,
                    "BOOKED"
                ))

                conn.execute("""
                    UPDATE akun_nusuk
                    SET status='BOOKED'
                    WHERE id=?
                """, (akun_id,))

                conn.commit()

                st.success("Booking berhasil")
                st.rerun()

    st.divider()

    # ======================
    # DATA BOOKING
    # ======================
    with st.container(border=True):

        st.subheader("Data Booking")

        df = pd.read_sql("""
            SELECT 
                b.id,
                a.name_identity,
                a.email,
                a.group_id,
                b.tanggal_booking
            FROM booking b
            JOIN akun_nusuk a ON b.akun_id=a.id
            WHERE b.user_id=?
            ORDER BY b.id DESC
        """, conn, params=(user["id"],))

        if df.empty:
            st.info("Belum ada booking")
            return

        df["tanggal_booking"] = pd.to_datetime(df["tanggal_booking"])

        # ======================
        # CANCEL MULTI
        # ======================
        df["Cancel"] = False

        edited_df = st.data_editor(df, use_container_width=True)

        if st.button("Cancel yang dipilih", use_container_width=True):

            selected_rows = edited_df[edited_df["Cancel"] == True]

            if selected_rows.empty:
                st.warning("Tidak ada yang dipilih")
            else:
                for _, row in selected_rows.iterrows():

                    conn.execute("""
                        UPDATE akun_nusuk
                        SET status='READY'
                        WHERE id IN (
                            SELECT akun_id FROM booking WHERE id=?
                        )
                    """, (row["id"],))

                    conn.execute("DELETE FROM booking WHERE id=?", (row["id"],))

                conn.commit()
                st.success("Booking berhasil dihapus")
                st.rerun()

    st.divider()

    # ======================
    # EDIT BOOKING
    # ======================
    with st.container(border=True):

        st.subheader("Edit Booking")

        selected_id = st.selectbox(
            "Pilih Booking",
            df["id"],
            format_func=lambda x: f"{df[df['id']==x]['name_identity'].values[0]}"
        )

        row = df[df["id"] == selected_id].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            new_tgl = st.date_input("Tanggal Baru", value=row["tanggal_booking"].date())

        with col2:
            new_jam = st.time_input("Jam Baru", value=row["tanggal_booking"].time())

        if st.button("Update Booking", use_container_width=True):

            conn.execute("""
                UPDATE booking
                SET tanggal_booking=?
                WHERE id=?
            """, (
                datetime.combine(new_tgl, new_jam),
                selected_id
            ))

            conn.commit()

            st.success("Booking berhasil diupdate")
            st.rerun()
