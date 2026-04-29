import streamlit as st
import pandas as pd
from utils.db import get_connection
from datetime import datetime

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
        ORDER BY 
            CASE WHEN type='LEADER' THEN 0 ELSE 1 END,
            name_identity ASC
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

    selected_akun = akun[akun["id"] == akun_id].iloc[0]
    selected_type = selected_akun["type"]
    selected_identity = selected_akun["name_identity"]

    # ======================
    # INPUT QTY
    # ======================
    qty = st.number_input("QTY", min_value=1, max_value=50, value=1)

    # ======================
    # VALIDASI
    # ======================
    if qty > 1 and selected_type != "LEADER":
        st.warning("QTY > 1 wajib pilih LEADER")
        return

    # ======================
    # INPUT TANGGAL
    # ======================
    col1, col2 = st.columns(2)

    with col1:
        tgl = st.date_input("Tanggal")

    with col2:
        jam = st.time_input("Jam")

    tanggal_booking = datetime.combine(tgl, jam)

    # ======================
    # BOOKING
    # ======================
    if st.button("Booking"):

        # ambil nomor group (misal: LEADER 05 → 05)
        try:
            nomor = selected_identity.split()[-1]
        except:
            st.error("Format name_identity salah (contoh: LEADER 01)")
            return

        # ======================
        # AMBIL MEMBER LANGSUNG DARI DB
        # ======================
        member_df = pd.read_sql("""
            SELECT id, name_identity
            FROM akun_nusuk
            WHERE user_id=?
            AND UPPER(gender)=UPPER(?)
            AND type='MEMBER'
            AND status='READY'
        """, conn, params=(user["id"], gender))

        # filter member sesuai nomor group
        member_df = member_df[
            member_df["name_identity"].str.endswith(nomor)
        ]

        # ======================
        # GABUNG LEADER + MEMBER
        # ======================
        final_ids = [akun_id]

        if qty > 1:
            if len(member_df) < (qty - 1):
                st.error(f"Member untuk group {nomor} tidak cukup ❌")
                return

            member_ids = member_df.head(qty - 1)["id"].tolist()
            final_ids.extend(member_ids)

        # ======================
        # INSERT BOOKING
        # ======================
        for acc_id in final_ids:

            conn.execute("""
                INSERT INTO booking 
                (user_id, akun_id, gender, tanggal_booking, qty, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user["id"],
                acc_id,
                gender,
                tanggal_booking.strftime("%Y-%m-%d %H:%M"),
                1,
                "BOOKED"
            ))

            # update akun jadi BOOKED
            conn.execute("""
                UPDATE akun_nusuk 
                SET status='BOOKED' 
                WHERE id=?
            """, (acc_id,))

        conn.commit()

        st.success(f"✅ Booking {len(final_ids)} akun berhasil (Group {nomor})")
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
