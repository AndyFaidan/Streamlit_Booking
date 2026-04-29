import streamlit as st
import pandas as pd
from utils.db import get_connection

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
    # FILTER USER (ROLE)
    # ======================
    if user["username"] != "andy":
        df = df[df["user_id"] == user["id"]]

    st.dataframe(df, use_container_width=True)

    st.divider()

    # ======================
    # PILIH DATA
    # ======================
    selected_id = st.selectbox(
        "Pilih Booking",
        df["id"],
        format_func=lambda x: f"{df[df['id']==x]['name_identity'].values[0]} | {df[df['id']==x]['email'].values[0]}"
    )

    selected = df[df["id"] == selected_id].iloc[0]

    st.divider()

    # ======================
    # EDIT SECTION
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

    tanggal = st.text_input("Tanggal Booking", value=selected["tanggal_booking"])

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

            # 🔥 LOGIC PENTING
            if status == "CANCEL":
                conn.execute("""
                    UPDATE akun_nusuk 
                    SET status='READY'
                    WHERE name_identity=?
                """, (selected["name_identity"],))

            conn.commit()
            st.success("Data berhasil diupdate")
            st.rerun()

    # ======================
    # DELETE
    # ======================
    with col2:
        if st.button("🗑️ Hapus Booking"):

            # balikin akun ke READY
            conn.execute("""
                UPDATE akun_nusuk 
                SET status='READY'
                WHERE name_identity=?
            """, (selected["name_identity"],))

            conn.execute("DELETE FROM booking WHERE id=?", (selected_id,))
            conn.commit()

            st.warning("Booking dihapus & akun dikembalikan ke READY")
            st.rerun()
