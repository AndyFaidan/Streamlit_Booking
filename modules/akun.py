import streamlit as st
import pandas as pd
from utils.db import get_connection

def show(gender):
    st.title(f"Akun {gender}")

    user = st.session_state.user
    conn = get_connection()

    # ======================
    # TABS
    # ======================
    tab1, tab2 = st.tabs(["REGISTER DATA", "TABLE DATA"])

    # ======================
    # TAB 1 - INPUT
    # ======================
    with tab1:

        st.subheader("Upload CSV")
        st.caption("Kolom: email,password,domain,type,name_identity,status,checklist")

        file = st.file_uploader("Upload CSV", key=f"upload_{gender}")

        if file:
            data = pd.read_csv(file)

            for _, r in data.iterrows():
                conn.execute("""
                    INSERT INTO akun_nusuk
                    (user_id, email, password, domain, gender, type, name_identity, status, checklist)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user["id"],
                    r["email"],
                    r["password"],
                    r["domain"],
                    gender,
                    r["type"],
                    r["name_identity"],
                    r.get("status", "READY"),
                    int(r.get("checklist", 0))
                ))

            conn.commit()
            st.success("Upload berhasil")

        st.divider()

        st.subheader("Tambah Manual")

        col1, col2 = st.columns(2)

        with col1:
            email = st.text_input("Email", key=f"email_{gender}")
            password = st.text_input("Password", key=f"pass_{gender}")

        with col2:
            domain = st.text_input("Domain", key=f"domain_{gender}")
            tipe = st.selectbox("Type", ["LEADER", "MEMBER"], key=f"type_{gender}")

        name = st.text_input("Name Identity ", key=f"name_{gender}")

        if st.button("Simpan", key=f"save_{gender}"):
            conn.execute("""
                INSERT INTO akun_nusuk
                (user_id, email, password, domain, gender, type, name_identity, status, checklist)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user["id"],
                email,
                password,
                domain,
                gender,
                tipe,
                name,
                "READY",
                0
            ))

            conn.commit()
            st.success("Data tersimpan")

   # ======================
# TAB 2 - TABLE + EDIT + DELETE
# ======================
# ======================
# TAB 2 - TABLE + FILTER + EDIT + DELETE
# ======================
    with tab2:

        st.subheader("Data Akun")

        df = pd.read_sql("""
            SELECT id, email, password, domain, gender, type, name_identity, status
            FROM akun_nusuk
            WHERE user_id=? AND gender=?
        """, conn, params=(user["id"], gender))

        if len(df) == 0:
            st.info("Belum ada data")
            return

        # ======================
        # FILTER SECTION
        # ======================
        col1, col2 = st.columns(2)

        with col1:
            search = st.text_input("🔍 Cari Email / Name")

        with col2:
            filter_type = st.selectbox("Filter Type", ["ALL", "LEADER", "MEMBER"])

        # apply filter
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
            "Pilih Data (untuk Edit / Delete)",
            df_filtered["id"],
            format_func=lambda x: df_filtered[df_filtered["id"] == x]["name_identity"].values[0]
        )

        selected_data = df_filtered[df_filtered["id"] == selected_id].iloc[0]

        st.divider()

        # ======================
        # EDIT SECTION
        # ======================
        st.subheader("✏️ Edit Data")

        col1, col2 = st.columns(2)

        with col1:
            email = st.text_input("Email", value=selected_data["email"])
            password = st.text_input("Password", value=selected_data["password"])

        with col2:
            domain = st.text_input("Domain", value=selected_data["domain"])
            tipe = st.selectbox("Type", ["LEADER", "MEMBER"],
                                index=0 if selected_data["type"] == "LEADER" else 1)

        name = st.text_input("Name Identity", value=selected_data["name_identity"])
        status = st.selectbox("Status", ["READY", "BOOKED"],
                            index=0 if selected_data["status"] == "READY" else 1)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Update Data"):
                conn.execute("""
                    UPDATE akun_nusuk SET
                        email=?,
                        password=?,
                        domain=?,
                        type=?,
                        name_identity=?,
                        status=?
                    WHERE id=?
                """, (
                    email,
                    password,
                    domain,
                    tipe,
                    name,
                    status,
                    selected_id
                ))
                conn.commit()
                st.success("Data berhasil diupdate")
                st.rerun()

        # ======================
        # DELETE SECTION
        # ======================
        with col2:
            if st.button("🗑️ Hapus Data"):
                conn.execute("DELETE FROM akun_nusuk WHERE id=?", (selected_id,))
                conn.commit()
                st.warning("Data berhasil dihapus")
                st.rerun()