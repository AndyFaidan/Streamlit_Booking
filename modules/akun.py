import streamlit as st
import pandas as pd
from utils.db import get_connection

# ======================
# DOMAIN LIST
# ======================
DOMAIN_LIST = [
    "GMAIL (LEADER)",
    "YAHOO (LEADER)",
    "ZOHOMAIL (LEADER)",
    "ATOMICMAIL (MEMBER)",
]

# ======================
# AUTO TYPE DARI DOMAIN
# ======================
def get_type(domain):
    domain = str(domain).upper()

    if "LEADER" in domain:
        return "LEADER"
    elif "MEMBER" in domain:
        return "MEMBER"
    else:
        return "MEMBER"


# ======================
# MAIN FUNCTION
# ======================
def show(gender):

    st.title(f"Akun {gender}")

    user = st.session_state.user
    conn = get_connection()

    tab1, tab2 = st.tabs(["REGISTER DATA", "TABLE DATA"])

    # ======================
    # TAB 1 - INPUT
    # ======================
    with tab1:

        st.subheader("Upload CSV")
        st.caption("Kolom wajib: email,domain,name_identity")

        file = st.file_uploader("Upload CSV", key=f"upload_{gender}")

        if file:
            data = pd.read_csv(file)

            for _, r in data.iterrows():

                domain = str(r["domain"])
                tipe = get_type(domain)

                conn.execute("""
                    INSERT INTO akun_nusuk
                    (user_id, email, domain, gender, type, name_identity, status, checklist)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user["id"],
                    r["email"],
                    domain,
                    gender,
                    tipe,
                    r["name_identity"],
                    r.get("status", "READY"),
                    int(r.get("checklist", 0))
                ))

            conn.commit()
            st.success("Upload berhasil ✅")
            st.rerun()

        st.divider()

        # ======================
        # INPUT MANUAL
        # ======================
        st.subheader("Tambah Manual")

        col1, col2 = st.columns(2)

        with col1:
            email = st.text_input("Email", key=f"email_{gender}")

        with col2:
            domain = st.selectbox("Domain", DOMAIN_LIST, key=f"domain_{gender}")
            tipe = get_type(domain)

        name = st.text_input("Name Identity", key=f"name_{gender}")

        st.info(f"Type otomatis: {tipe}")

        if st.button("Simpan", key=f"save_{gender}"):

            conn.execute("""
                INSERT INTO akun_nusuk
                (user_id, email, domain, gender, type, name_identity, status, checklist)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user["id"],
                email,
                domain,
                gender,
                tipe,
                name,
                "READY",
                0
            ))

            conn.commit()
            st.success("Data tersimpan ✅")
            st.rerun()

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

        selected_data = df_filtered[df_filtered["id"] == selected_id].iloc[0]

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

        with col1:
            if st.button("💾 Update Data"):

                conn.execute("""
                    UPDATE akun_nusuk SET
                        email=?,
                        domain=?,
                        type=?,
                        name_identity=?,
                        status=?
                    WHERE id=?
                """, (
                    email,
                    domain,
                    tipe,
                    name,
                    status,
                    selected_id
                ))

                conn.commit()
                st.success("Data berhasil diupdate ✅")
                st.rerun()

        with col2:
            if st.button("🗑️ Hapus Data"):

                conn.execute("DELETE FROM akun_nusuk WHERE id=?", (selected_id,))
                conn.commit()

                st.warning("Data berhasil dihapus")
                st.rerun()
