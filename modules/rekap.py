import streamlit as st
import pandas as pd
from utils.db import get_connection

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
    if user["role"] == "admin":
        st.success("Mode Admin: Melihat semua data")
    else:
        df = df[df["user_id"] == user["id"]]
        st.info("Mode User: Hanya melihat data sendiri")

    if df.empty:
        st.info("Tidak ada data")
        return

    # ======================
    # TAMBAH NAMA USER
    # ======================
    df["user_name"] = df["user_id"].map(USER_MAP)

    # ======================
    # SUMMARY
    # ======================
    total_booking = len(df)
    total_pax = df["qty"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Booking", total_booking)
    col2.metric("Total Pax", total_pax)

    st.divider()

    # ======================
    # TABLE
    # ======================
    st.dataframe(df[[
        "user_name",
        "name_identity",
        "email",
        "gender",
        "type",
        "qty",
        "tanggal_booking",
        "status"
    ]], use_container_width=True)

    st.divider()

    # ======================
    # SELECT DATA
    # ======================
    selected_id = st.selectbox(
        "Pilih Booking",
        df["id"],
        format_func=lambda x: f"{df[df['id']==x]['name_identity'].values[0]} | {df[df['id']==x]['email'].values[0]}"
    )

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
        qty = st.number_input("Qty", min_value=1, max_value=100, value=int(selected["qty"]))

    with col2:
        status = st.selectbox(
            "Status",
            ["BOOKED", "CANCEL"],
            index=0 if selected["status"] == "BOOKED" else 1
        )

    tanggal = st.text_input("Tanggal Booking", value=str(selected["tanggal_booking"]))

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
            """, (qty, tanggal, status, selected_id))

            if status == "CANCEL":
                conn.execute("""
                    UPDATE akun_nusuk 
                    SET status='READY'
                    WHERE id=?
                """, (selected["akun_id"],))

            conn.commit()
            st.success("Data berhasil diupdate")
            st.rerun()

    # ======================
    # DELETE
    # ======================
    with col2:
        if st.button("🗑️ Hapus Booking"):

            conn.execute("""
                UPDATE akun_nusuk 
                SET status='READY'
                WHERE id=?
            """, (selected["akun_id"],))

            conn.execute("DELETE FROM booking WHERE id=?", (selected_id,))
            conn.commit()

            st.warning("Booking dihapus")
            st.rerun()
