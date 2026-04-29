import streamlit as st
import pandas as pd
from utils.db import get_connection
from datetime import datetime
import re

def show():
    st.title("Booking")

    user = st.session_state.user
    conn = get_connection()

    # ======================
    # PILIH GENDER
    # ======================
    gender = st.selectbox("Pilih Gender", ["PRIA", "WANITA"])

    # ======================
    # AMBIL AKUN READY
    # ======================
    akun = pd.read_sql("""
        SELECT id, name_identity, email, type
        FROM akun_nusuk 
        WHERE user_id=? 
        AND UPPER(gender)=UPPER(?) 
        AND status='READY'
        ORDER BY CASE WHEN type='LEADER' THEN 0 ELSE 1 END
    """, conn, params=(user["id"], gender))

    if akun.empty:
        st.warning(f"Tidak ada akun READY untuk {gender}")
        return

    # ======================
    # DROPDOWN AKUN
    # ======================
    akun_map = {
        f"{row['name_identity']} ({row['type']}) | {row['email']}": row["id"]
        for _, row in akun.iterrows()
    }

    selected = st.selectbox("Pilih Akun", list(akun_map.keys()))
    akun_id = akun_map[selected]

    selected_akun = akun[akun["id"] == akun_id]

    if selected_akun.empty:
        st.error("Akun tidak ditemukan")
        return

    selected_type = selected_akun.iloc[0]["type"]
    selected_identity = selected_akun.iloc[0]["name_identity"]

    # ======================
    # INPUT QTY
    # ======================
    qty = st.number_input("QTY", min_value=1, max_value=50, value=1)

    # ======================
    # VALIDASI LEADER
    # ======================
    if qty > 1 and selected_type != "LEADER":
        st.warning("QTY > 1 harus pilih LEADER")
        return

    # ======================
    # INPUT TANGGAL + JAM
    # ======================
    col1, col2 = st.columns(2)

    with col1:
        tgl = st.date_input("Tanggal")

    with col2:
        jam = st.time_input("Jam")

    tanggal_booking = datetime.combine(tgl, jam)

    # ======================
    # BUTTON BOOKING
    # ======================
    if st.button("Booking"):

        # ======================
        # AMBIL NOMOR GROUP (AMAN)
        # ======================
        match = re.search(r'\d+$', str(selected_identity))

        if not match:
            st.error("Format name_identity harus ada nomor (contoh: LEADER 05)")
            return

        nomor = match.group()  # ex: 05

        # ======================
        # JIKA QTY = 1
        # ======================
        if qty == 1:
            final_akun = selected_akun.copy()

        else:
            # ======================
            # AMBIL MEMBER SESUAI GROUP (FIXED)
            # ======================
            member = akun[
                (akun["type"] == "MEMBER") &
                (akun["name_identity"].str.endswith(f" {nomor}")) &
                (akun["id"] != akun_id)
            ].head(qty - 1)

            final_akun = pd.concat([selected_akun, member])

            # VALIDASI JUMLAH
            if len(final_akun) < qty:
                st.error(f"Member group {nomor} tidak cukup")
                return

        # ======================
        # SIMPAN BOOKING
        # ======================
        inserted = 0

        for _, row in final_akun.iterrows():

            # CEK SUDAH BOOKED
            cek = pd.read_sql(
                "SELECT id FROM booking WHERE akun_id=? AND status='BOOKED'",
                conn,
                params=(row["id"],)
            )

            if len(cek) > 0:
                continue  # skip kalau sudah dibooking

            conn.execute("""
                INSERT INTO booking 
                (user_id, akun_id, gender, tanggal_booking, qty, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user["id"],
                row["id"],
                gender,
                tanggal_booking.strftime("%Y-%m-%d %H:%M"),
                1,
                "BOOKED"
            ))

            # UPDATE STATUS AKUN
            conn.execute("""
                UPDATE akun_nusuk 
                SET status='BOOKED' 
                WHERE id=?
            """, (row["id"],))

            inserted += 1

        conn.commit()

        if inserted == 0:
            st.warning("Semua akun sudah pernah dibooking")
        else:
            st.success(f"✅ Booking {inserted} akun berhasil (Group {nomor})")

        st.rerun()

    st.divider()

    # ======================
    # DATA BOOKING
    # ======================
    st.subheader("Data Booking")

    df = pd.read_sql("""
        SELECT 
            b.id,
            a.name_identity,
            a.email,
            a.type,
            b.gender,
            b.qty,
            b.tanggal_booking,
            b.status
        FROM booking b
        JOIN akun_nusuk a ON b.akun_id = a.id
        WHERE b.user_id=?
        ORDER BY b.tanggal_booking DESC
    """, conn, params=(user["id"],))

    st.dataframe(df, use_container_width=True)
