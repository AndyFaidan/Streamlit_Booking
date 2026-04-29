import streamlit as st
import pandas as pd
from utils.db import get_connection
from datetime import datetime

# ======================
# USER MAP
# ======================
USER_MAP = {
    1: "Andy Sofyan Guspriyanto",
    2: "Peri Romadon",
    3: "Arief Zaenal Hakim"
}

def show():
    st.title("Rekapan Booking")

    user = st.session_state.user
    conn = get_connection()

    # ======================
    # LOAD DATA
    # ======================
    df = pd.read_sql("""
        SELECT 
            b.id,
            b.user_id,
            b.akun_id,
            a.email,
            a.gender,
            a.type,
            a.name_identity,
            b.qty,
            b.tanggal_booking,
            b.status
        FROM booking b
        JOIN akun_nusuk a ON b.akun_id = a.id
        ORDER BY b.tanggal_booking DESC
    """, conn)

    if df.empty:
        st.info("Belum ada data booking")
        return

    # ======================
    # ROLE FILTER
    # ======================
    if user["role"] != "admin":
        df = df[df["user_id"] == user["id"]]
        st.info("Mode User: hanya data sendiri")
    else:
        st.success("Mode Admin: semua data")

    if df.empty:
        st.info("Tidak ada data")
        return

    # ======================
    # MAP USER
    # ======================
    df["user_name"] = df["user_id"].map(USER_MAP)

    # ======================
    # SUMMARY
    # ======================
    col1, col2 = st.columns(2)
    col1.metric("Total Booking", len(df))
    col2.metric("Total Pax", int(df["qty"].sum()))

    st.divider()

    # ======================
    # TABLE
    # ======================
    st.dataframe(df, use_container_width=True)

    st.divider()

    # ======================
    # SAFE SELECT
    # ======================
    options = {
        f"{row['name_identity']} | {row['email']} | {row['tanggal_booking']}": row["id"]
        for _, row in df.iterrows()
    }

    selected_label = st.selectbox("Pilih Booking", list(options.keys()))
    selected_id = options[selected_label]

    selected_df = df[df["id"] == selected_id]

    if selected_df.empty:
        st.warning("Data tidak ditemukan")
        st.stop()

    selected = selected_df.iloc[0]

    st.divider()

    # ======================
    # EDIT
    # ======================
    st.subheader("✏️ Edit Booking")

    col1, col2 = st.columns(2)

    with col1:
        qty = st.number_input("Qty", 1, 100, int(selected["qty"]))

    with col2:
        status = st.selectbox(
            "Status",
            ["BOOKED", "CANCEL"],
            index=0 if selected["status"] == "BOOKED" else 1
        )

    # gunakan datetime picker (lebih aman)
    tanggal = st.datetime_input(
        "Tanggal Booking",
        value=pd.to_datetime(selected["tanggal_booking"])
    )

    col1, col2 = st.columns(2)

    # ======================
    # UPDATE
    # ======================
    with col1:
        if st.button("💾 Update"):

            conn.execute("""
                UPDATE booking
                SET qty=?, tanggal_booking=?, status=?
                WHERE id=?
            """, (
                qty,
                tanggal.strftime("%Y-%m-%d %H:%M"),
                status,
                selected_id
            ))

            # ======================
            # SYNC AKUN
            # ======================
            if status == "CANCEL":
                conn.execute("""
                    UPDATE akun_nusuk
                    SET status='READY'
                    WHERE id=?
                """, (selected["akun_id"],))

            elif status == "BOOKED":
                conn.execute("""
                    UPDATE akun_nusuk
                    SET status='BOOKED'
                    WHERE id=?
                """, (selected["akun_id"],))

            conn.commit()

            st.success("Update berhasil ✅")
            st.rerun()

    # ======================
    # DELETE
    # ======================
    with col2:
        if st.button("🗑️ Hapus Booking"):

            # kembalikan akun ke READY
            conn.execute("""
                UPDATE akun_nusuk
                SET status='READY'
                WHERE id=?
            """, (selected["akun_id"],))

            conn.execute("DELETE FROM booking WHERE id=?", (selected_id,))
            conn.commit()

            st.warning("Booking dihapus & akun kembali READY")
            st.rerun()
