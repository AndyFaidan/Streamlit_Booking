import streamlit as st
import pandas as pd
from utils.db import get_connection
from datetime import datetime

def show():
    st.title("📅 Booking (Auto Gender)")

    conn = get_connection()
    user = st.session_state.user

    # ======================
    # PILIH GENDER
    # ======================
    gender = st.selectbox(
        "Pilih Gender",
        ["PRIA", "WANITA"],
        key="gender_booking"
    )

    # ======================
    # AMBIL AKUN READY
    # ======================
    akun = pd.read_sql("""
        SELECT * FROM akun_nusuk
        WHERE user_id=? 
        AND status='READY'
        AND gender=?
    """, conn, params=(user["id"], gender))

    if akun.empty:
        st.warning(f"Tidak ada akun READY untuk {gender}")
    else:
        # ======================
        # PILIH AKUN
        # ======================
        akun_map = {
            f"{r['name_identity']} | {r['email']} (G{r['group_id']})": r["id"]
            for _, r in akun.iterrows()
        }

        selected = st.selectbox(
            "Pilih Akun",
            list(akun_map.keys()),
            key=f"select_booking_{gender}"
        )

        akun_id = akun_map[selected]

        # ======================
        # INPUT TANGGAL
        # ======================
        col1, col2 = st.columns(2)

        with col1:
            tgl = st.date_input("Tanggal", key=f"tgl_{gender}")

        with col2:
            jam = st.time_input("Jam", key=f"jam_{gender}")

        # ======================
        # BOOKING
        # ======================
        if st.button("🚀 Booking", key=f"btn_booking_{gender}"):

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

            st.success(f"Booking {gender} berhasil ✅")
            st.rerun()

    st.divider()

    # ======================
    # DATA BOOKING
    # ======================
    st.subheader(f"📊 Data Booking {gender}")

    df = pd.read_sql("""
        SELECT 
            b.id,
            a.name_identity,
            a.email,
            a.group_id,
            b.tanggal_booking
        FROM booking b
        JOIN akun_nusuk a ON b.akun_id=a.id
        WHERE b.user_id=? AND b.gender=?
        ORDER BY b.id DESC
    """, conn, params=(user["id"], gender))

    if df.empty:
        st.info("Belum ada booking")

    # convert tanggal
    df["tanggal_booking"] = pd.to_datetime(df["tanggal_booking"], errors='coerce')

    # ======================
    # CHECKLIST CANCEL
    # ======================
    if not df.empty:

        df["Cancel?"] = False

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            key=f"editor_{gender}"
        )

        # ======================
        # CANCEL MULTI
        # ======================
        if st.button("❌ Cancel yang dipilih", key=f"cancel_{gender}"):

            selected_rows = edited_df[edited_df["Cancel?"] == True]

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

                st.success(f"{len(selected_rows)} booking di-cancel ✅")
                st.rerun()

    st.divider()

    # ======================
    # EDIT BOOKING
    # ======================
    st.subheader("✏️ Edit Booking")

    if df.empty:
        st.warning("Tidak ada data untuk diedit")
        return

    selected_id = st.selectbox(
        "Pilih Booking",
        df["id"],
        format_func=lambda x: f"{df[df['id']==x]['name_identity'].values[0]} | {df[df['id']==x]['email'].values[0]}",
        key=f"edit_select_{gender}"
    )

    row = df[df["id"] == selected_id].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        new_tgl = st.date_input(
            "Tanggal Baru",
            value=row["tanggal_booking"].date(),
            key=f"edit_tgl_{gender}"
        )

    with col2:
        new_jam = st.time_input(
            "Jam Baru",
            value=row["tanggal_booking"].time(),
            key=f"edit_jam_{gender}"
        )

    if st.button("💾 Update Booking", key=f"update_{gender}"):

        conn.execute("""
            UPDATE booking
            SET tanggal_booking=?
            WHERE id=?
        """, (
            datetime.combine(new_tgl, new_jam),
            selected_id
        ))

        conn.commit()

        st.success("Booking berhasil diupdate ✅")
        st.rerun()
