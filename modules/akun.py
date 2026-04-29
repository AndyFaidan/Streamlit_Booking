# ======================
# TAB 2 - TABLE
# ======================
with tab2:

    st.subheader("Data Akun")

    df = pd.read_sql("""
        SELECT id, email, domain, gender, type, name_identity, status
        FROM akun_nusuk
        WHERE user_id=? AND gender=?
    """, conn, params=(user["id"], gender))

    if len(df) == 0:
        st.info("Belum ada data")
        return

    # ======================
    # FILTER
    # ======================
    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input("🔍 Cari Email / Name")

    with col2:
        filter_type = st.selectbox("Filter Type", ["ALL", "LEADER", "MEMBER"])

    df_filtered = df.copy()

    if search:
        df_filtered = df_filtered[
            df_filtered["email"].str.contains(search, case=False) |
            df_filtered["name_identity"].str.contains(search, case=False)
        ]

    if filter_type != "ALL":
        df_filtered = df_filtered[df_filtered["type"] == filter_type]

    st.dataframe(df_filtered, use_container_width=True)

    st.divider()

    # ======================
    # PILIH DATA
    # ======================
    selected_id = st.selectbox(
        "Pilih Data",
        df_filtered["id"],
        format_func=lambda x: df_filtered[df_filtered["id"] == x]["name_identity"].values[0]
    )

    selected_df = df_filtered[df_filtered["id"] == selected_id]

    if selected_df.empty:
        st.warning("Data tidak ditemukan")
        st.stop()

    selected_data = selected_df.iloc[0]

    st.divider()

    # ======================
    # EDIT
    # ======================
    st.subheader("✏️ Edit Data")

    col1, col2 = st.columns(2)

    with col1:
        email = st.text_input("Email", value=selected_data["email"])

    with col2:
        domain = st.selectbox(
            "Domain",
            DOMAIN_LIST,
            index=DOMAIN_LIST.index(selected_data["domain"]) if selected_data["domain"] in DOMAIN_LIST else 0
        )
        tipe = get_type(domain)

    name = st.text_input("Name Identity", value=selected_data["name_identity"])

    status = st.selectbox(
        "Status",
        ["READY", "BOOKED"],
        index=0 if selected_data["status"] == "READY" else 1
    )

    st.info(f"Type otomatis: {tipe}")

    col1, col2 = st.columns(2)

    # ======================
    # UPDATE (FIX UTAMA)
    # ======================
    with col1:
        if st.button("💾 Update Data"):

            # update akun
            conn.execute("""
                UPDATE akun_nusuk SET
                    email=?, 
                    domain=?, 
                    type=?, 
                    name_identity=?, 
                    status=?
                WHERE id=?
            """, (
                email, domain, tipe, name, status, selected_id
            ))

            # ======================
            # SYNC BOOKING
            # ======================
            if status == "READY":
                # semua booking akun ini jadi CANCEL
                conn.execute("""
                    UPDATE booking
                    SET status='CANCEL'
                    WHERE akun_id=?
                """, (selected_id,))

            elif status == "BOOKED":
                # jika tidak ada booking → buat dummy (optional)
                check = pd.read_sql("""
                    SELECT * FROM booking WHERE akun_id=? AND status='BOOKED'
                """, conn, params=(selected_id,))

                if len(check) == 0:
                    conn.execute("""
                        INSERT INTO booking 
                        (user_id, akun_id, gender, tanggal_booking, qty, status)
                        VALUES (?, ?, ?, datetime('now'), ?, ?)
                    """, (
                        user["id"],
                        selected_id,
                        gender,
                        1,
                        "BOOKED"
                    ))

            conn.commit()
            st.success("Data berhasil diupdate & sinkron ✅")
            st.rerun()

    # ======================
    # DELETE
    # ======================
    with col2:
        if st.button("🗑️ Hapus Data"):

            # hapus booking dulu
            conn.execute("DELETE FROM booking WHERE akun_id=?", (selected_id,))

            # hapus akun
            conn.execute("DELETE FROM akun_nusuk WHERE id=?", (selected_id,))

            conn.commit()

            st.warning("Data akun & booking terhapus")
            st.rerun()

    # ======================
    # DELETE ALL
    # ======================
    st.divider()
    st.subheader("⚠️ Hapus Semua Data")

    confirm = st.text_input("Ketik 'HAPUS' untuk konfirmasi")

    if confirm == "HAPUS":
        if st.button("🗑️ Hapus Semua", use_container_width=True):

            # hapus booking dulu
            conn.execute("""
                DELETE FROM booking 
                WHERE akun_id IN (
                    SELECT id FROM akun_nusuk 
                    WHERE user_id=? AND gender=?
                )
            """, (user["id"], gender))

            # hapus akun
            conn.execute("""
                DELETE FROM akun_nusuk 
                WHERE user_id=? AND gender=?
            """, (user["id"], gender))

            conn.commit()

            st.success("Semua data terhapus ✅")
            st.rerun()
