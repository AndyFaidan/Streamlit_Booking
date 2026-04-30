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
    "ZOHOMAIL (LEADER)",
    "ATOMICMAIL (MEMBER)",
]

STATUS_LIST = ["READY", "BOOKED", "USED"]

# ======================
# TYPE OTOMATIS
# ======================
def get_type(domain):
    return "LEADER" if "LEADER" in str(domain).upper() else "MEMBER"

# ======================
# EXTRACT GROUP ID
# ======================
def extract_group(name):
    match = re.search(r'(\d+)$', str(name))
    return match.group(1) if match else None

# ======================
# NORMALIZE DATA
# ======================
def normalize_row(r):
    email = str(r["email"]).strip().lower()
    domain = str(r["domain"]).strip().upper().replace(" ", "")
    name = str(r["name_identity"]).strip().upper()
    tipe = get_type(domain)
    group_id = extract_group(name)
    return email, domain, name, tipe, group_id

# ======================
# MAIN FUNCTION
# ======================
def show(gender):

    st.title(f"📂 Akun {gender}")

    conn = get_connection()
    user = st.session_state.user

    tab1, tab2 = st.tabs(["📥 Upload & Input", "📊 Data Akun"])

    # ======================
    # TAB 1 - UPLOAD & INPUT
    # ======================
    with tab1:

        st.subheader("Upload CSV")
        file = st.file_uploader("Upload CSV", type=["csv"], key=f"upload_{gender}")

        if file:
            df = pd.read_csv(file)

            st.dataframe(df, use_container_width=True)

            if st.button("🚀 Proses Upload", key=f"upload_btn_{gender}"):

                inserted, skipped = 0, 0

                for _, r in df.iterrows():

                    email, domain, name, tipe, group_id = normalize_row(r)

                    if not group_id:
                        skipped += 1
                        continue

                    cek = conn.execute("""
                        SELECT id FROM akun_nusuk
                        WHERE user_id=? AND email=? AND gender=?
                    """, (user["id"], email, gender)).fetchone()

                    if cek:
                        skipped += 1
                        continue

                    try:
                        conn.execute("""
                            INSERT INTO akun_nusuk
                            (user_id, email, domain, gender, type, name_identity, group_id, status, checklist)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            user["id"],
                            email,
                            domain,
                            gender,
                            tipe,
                            name,
                            group_id,
                            "READY",
                            0
                        ))
                        inserted += 1
                    except:
                        skipped += 1

                conn.commit()
                st.success(f"✅ Insert: {inserted} | Skip: {skipped}")
                st.rerun()

        st.divider()

        # ======================
        # INPUT MANUAL
        # ======================
        st.subheader("Tambah Manual")

        email = st.text_input("Email", key=f"email_{gender}")
        domain = st.selectbox("Domain", DOMAIN_LIST, key=f"domain_{gender}")
        tipe = get_type(domain)

        name = st.text_input("Name Identity (LEADER 01)", key=f"name_{gender}")
        group_id = extract_group(name)

        st.info(f"Type: {tipe} | Group: {group_id}")

        if st.button("💾 Simpan", key=f"save_{gender}"):

            if not email or not group_id:
                st.warning("Data belum lengkap")
                return

            cek = conn.execute("""
                SELECT id FROM akun_nusuk
                WHERE user_id=? AND email=? AND gender=?
            """, (user["id"], email, gender)).fetchone()

            if cek:
                st.error("Email sudah ada")
                return

            conn.execute("""
                INSERT INTO akun_nusuk
                (user_id, email, domain, gender, type, name_identity, group_id, status, checklist)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user["id"],
                email.lower(),
                domain,
                gender,
                tipe,
                name.upper(),
                group_id,
                "READY",
                0
            ))

            conn.commit()
            st.success("Data tersimpan")
            st.rerun()

    # ======================
    # TAB 2 - DATA
    # ======================
    with tab2:

        df = pd.read_sql("""
            SELECT id, email, domain, type, name_identity, group_id, status
            FROM akun_nusuk
            WHERE user_id=? AND gender=?
        """, conn, params=(user["id"], gender))

        if df.empty:
            st.info("Belum ada data")
            return

        search = st.text_input("🔍 Cari")

        if search:
            df = df[
                df["email"].str.contains(search, case=False) |
                df["name_identity"].str.contains(search, case=False)
            ]

        st.dataframe(df, use_container_width=True)

        st.divider()

        # ======================
        # SELECT DATA (FIXED)
        # ======================
        if "selected_id" not in st.session_state:
            st.session_state.selected_id = df["id"].iloc[0]

        selected_id = st.selectbox(
            "Pilih Data",
            df["id"],
            index=list(df["id"]).index(st.session_state.selected_id),
            format_func=lambda x: df[df["id"] == x]["name_identity"].values[0],
            key=f"select_{gender}"
        )

        st.session_state.selected_id = selected_id

        selected = df[df["id"] == selected_id].iloc[0]

        st.success(f"Edit: {selected['name_identity']}")

        # ======================
        # FORM EDIT (AUTO REFRESH)
        # ======================
        email = st.text_input(
            "Email",
            value=selected["email"],
            key=f"edit_email_{gender}_{selected_id}"
        )

        domain = st.selectbox(
            "Domain",
            DOMAIN_LIST,
            index=DOMAIN_LIST.index(selected["domain"]) if selected["domain"] in DOMAIN_LIST else 0,
            key=f"edit_domain_{gender}_{selected_id}"
        )

        tipe = get_type(domain)

        name = st.text_input(
            "Name Identity",
            value=selected["name_identity"],
            key=f"edit_name_{gender}_{selected_id}"
        )

        status = st.selectbox(
            "Status",
            STATUS_LIST,
            index=STATUS_LIST.index(selected["status"]) if selected["status"] in STATUS_LIST else 0,
            key=f"edit_status_{gender}_{selected_id}"
        )

        group_id = extract_group(name)

        col1, col2 = st.columns(2)

        # ======================
        # UPDATE
        # ======================
        with col1:
            if st.button("💾 Update", key=f"update_{gender}"):

                conn.execute("""
                    UPDATE akun_nusuk SET
                        email=?,
                        domain=?,
                        type=?,
                        name_identity=?,
                        group_id=?,
                        status=?
                    WHERE id=?
                """, (
                    email.lower(),
                    domain,
                    tipe,
                    name.upper(),
                    group_id,
                    status,
                    selected_id
                ))

                conn.commit()
                st.success("Update berhasil")
                st.rerun()

        # ======================
        # DELETE
        # ======================
        with col2:
            if st.button("🗑️ Hapus", key=f"delete_{gender}"):

                conn.execute("DELETE FROM akun_nusuk WHERE id=?", (selected_id,))
                conn.commit()

                st.warning("Data dihapus")
                st.rerun()
