import streamlit as st
import pandas as pd
from utils.db import get_connection
import re

# ======================
# DOMAIN LIST
# ======================
DOMAIN_LIST = [
    "GMAIL (LEADER)",
    "YAHOO (LEADER)",
    "ATOMICMAIL (MEMBER)",
]

# ======================
# AUTO TYPE
# ======================
def get_type(domain):
    return "LEADER" if "LEADER" in domain else "MEMBER"

# ======================
# NORMALIZE NAME
# ======================
def normalize(name):
    name = name.strip().upper()
    match = re.search(r'(\d+)$', name)

    if not match:
        return name, None

    num = match.group(1).zfill(2)
    tipe = "LEADER" if "LEADER" in name else "MEMBER"

    return f"{tipe} {num}", num


# ======================
# MAIN FUNCTION
# ======================
def show(gender):

    st.title(f"📧 Akun {gender}")

    conn = get_connection()
    user = st.session_state.user

    tab1, tab2 = st.tabs(["➕ Registrasi", "📊 Data Akun"])

    # ======================
    # TAB 1: REGISTRASI
    # ======================
    with tab1:

        st.subheader("📤 Upload CSV")
        st.caption("Format: email,domain,name_identity")

        file = st.file_uploader("Upload CSV", type=["csv"], key=f"upload_{gender}")

        if file:
            data = pd.read_csv(file)

            for _, r in data.iterrows():
                name, gid = normalize(r["name_identity"])

                conn.execute("""
                    INSERT INTO akun_nusuk
                    (user_id,email,domain,gender,type,name_identity,group_id,status,checklist)
                    VALUES (?,?,?,?,?,?,?,?,?)
                """, (
                    user["id"],
                    r["email"],
                    r["domain"],
                    gender,
                    get_type(r["domain"]),
                    name,
                    gid,
                    "READY",
                    0
                ))

            conn.commit()
            st.success("✅ Upload berhasil")
            st.rerun()

        st.divider()

        # ======================
        # INPUT MANUAL
        # ======================
        st.subheader("➕ Tambah Manual")

        col1, col2 = st.columns(2)

        with col1:
            email = st.text_input("Email", key=f"email_{gender}")

        with col2:
            domain = st.selectbox(
                "Domain",
                DOMAIN_LIST,
                key=f"domain_{gender}"
            )

        name = st.text_input(
            "Name Identity (contoh: LEADER 01)",
            key=f"name_{gender}"
        )

        tipe = get_type(domain)
        st.info(f"Type otomatis: {tipe}")

        if st.button("💾 Simpan", key=f"save_{gender}", use_container_width=True):

            if not email or not name:
                st.warning("⚠️ Isi semua field")
                return

            name, gid = normalize(name)

            conn.execute("""
                INSERT INTO akun_nusuk
                (user_id,email,domain,gender,type,name_identity,group_id,status,checklist)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                user["id"],
                email,
                domain,
                gender,
                tipe,
                name,
                gid,
                "READY",
                0
            ))

            conn.commit()
            st.success("Data tersimpan ✅")
            st.rerun()

    # ======================
    # TAB 2: TABLE + EDIT
    # ======================
    with tab2:

        st.subheader("📊 Data Akun")

        df = pd.read_sql("""
            SELECT id, email, domain, type, name_identity, group_id, status
            FROM akun_nusuk
            WHERE user_id=? AND gender=?
        """, conn, params=(user["id"], gender))

        if df.empty:
            st.info("Belum ada data")
            return

        # ======================
        # FILTER
        # ======================
        col1, col2 = st.columns(2)

        with col1:
            search = st.text_input("🔍 Cari", key=f"search_{gender}")

        with col2:
            filter_type = st.selectbox(
                "Filter",
                ["ALL", "LEADER", "MEMBER"],
                key=f"filter_{gender}"
            )

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
            format_func=lambda x: df_filtered[df_filtered["id"] == x]["name_identity"].values[0],
            key=f"select_{gender}"
        )

        row = df_filtered[df_filtered["id"] == selected_id].iloc[0]

        st.divider()
        st.subheader("✏️ Edit Data")

        col1, col2 = st.columns(2)

        with col1:
            email_edit = st.text_input(
                "Email",
                value=row["email"],
                key=f"email_edit_{gender}"
            )

        with col2:
            domain_edit = st.selectbox(
                "Domain",
                DOMAIN_LIST,
                index=DOMAIN_LIST.index(row["domain"]) if row["domain"] in DOMAIN_LIST else 0,
                key=f"domain_edit_{gender}"
            )

        name_edit = st.text_input(
            "Name Identity",
            value=row["name_identity"],
            key=f"name_edit_{gender}"
        )

        status_edit = st.selectbox(
            "Status",
            ["READY", "BOOKED", "USED"],
            index=["READY", "BOOKED", "USED"].index(row["status"]),
            key=f"status_edit_{gender}"
        )

        tipe_edit = get_type(domain_edit)
        st.info(f"Type otomatis: {tipe_edit}")

        col1, col2 = st.columns(2)

        # ======================
        # UPDATE
        # ======================
        with col1:
            if st.button("💾 Update", key=f"update_{gender}", use_container_width=True):

                name_edit, gid = normalize(name_edit)

                conn.execute("""
                    UPDATE akun_nusuk
                    SET email=?, domain=?, type=?, name_identity=?, group_id=?, status=?
                    WHERE id=?
                """, (
                    email_edit,
                    domain_edit,
                    tipe_edit,
                    name_edit,
                    gid,
                    status_edit,
                    selected_id
                ))

                conn.commit()
                st.success("Update berhasil ✅")
                st.rerun()

        # ======================
        # DELETE
        # ======================
        with col2:
            if st.button("🗑️ Hapus", key=f"delete_{gender}", use_container_width=True):

                conn.execute("DELETE FROM akun_nusuk WHERE id=?", (selected_id,))
                conn.commit()

                st.warning("Data dihapus")
                st.rerun()
