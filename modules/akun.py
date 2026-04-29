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
# AUTO TYPE
# ======================
def get_type(domain):
    domain = str(domain).upper()

    if "LEADER" in domain:
        return "LEADER"
    elif "MEMBER" in domain:
        return "MEMBER"
    return "MEMBER"


# ======================
# MAIN
# ======================
def show(gender):

    st.title(f"Akun {gender}")

    user = st.session_state.user
    conn = get_connection()

    tab1, tab2 = st.tabs(["REGISTER DATA", "TABLE DATA"])

    # ======================
    # INIT FLAG (ANTI LOOP)
    # ======================
    if f"uploaded_{gender}" not in st.session_state:
        st.session_state[f"uploaded_{gender}"] = False

    # ======================
    # TAB 1 - INPUT
    # ======================
    with tab1:

        st.subheader("Upload CSV")
        st.caption("Kolom wajib: email,domain,name_identity")

        file = st.file_uploader("Upload CSV", key=f"upload_{gender}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🚀 Proses Upload", use_container_width=True):

                if file is None:
                    st.warning("Upload file dulu")
                elif st.session_state[f"uploaded_{gender}"]:
                    st.info("File sudah pernah diupload, klik reset jika ingin ulang")
                else:

                    data = pd.read_csv(file)

                    # ambil email existing
                    existing = pd.read_sql("""
                        SELECT email FROM akun_nusuk 
                        WHERE user_id=? AND gender=?
                    """, conn, params=(user["id"], gender))

                    existing_emails = set(existing["email"])

                    inserted = 0
                    skipped = 0

                    for _, r in data.iterrows():

                        email = str(r["email"])

                        if email in existing_emails:
                            skipped += 1
                            continue

                        domain = str(r["domain"])
                        tipe = get_type(domain)

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
                            r["name_identity"],
                            r.get("status", "READY"),
                            int(r.get("checklist", 0))
                        ))

                        inserted += 1

                    conn.commit()

                    st.session_state[f"uploaded_{gender}"] = True

                    st.success(f"✅ Upload selesai | Insert: {inserted} | Skip: {skipped}")
                    st.rerun()

        with col2:
            if st.button("🔄 Reset Upload", use_container_width=True):
                st.session_state[f"uploaded_{gender}"] = False
                st.success("Upload direset")

        st.divider()

        # ======================
        # MANUAL INPUT
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

            # cek duplikat
            check = pd.read_sql("""
                SELECT * FROM akun_nusuk 
                WHERE email=? AND user_id=? AND gender=?
            """, conn, params=(email, user["id"], gender))

            if len(check) > 0:
                st.warning("Email sudah ada ❌")
            else:
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
        # SELECT
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
                # SYNC DENGAN BOOKING
                # ======================
                if status == "READY":
                    # kalau dibalikin READY → booking jadi CANCEL
                    conn.execute("""
                        UPDATE booking
                        SET status='CANCEL'
                        WHERE akun_id=?
                    """, (selected_id,))
            
                elif status == "BOOKED":
                    # kalau dipaksa BOOKED → buat booking dummy (opsional)
                    pass
            
                conn.commit()
            
                st.success("Data berhasil diupdate ✅ (sync dengan booking)")
                st.rerun()

        with col2:
            if st.button("🗑️ Hapus Data"):
                conn.execute("DELETE FROM akun_nusuk WHERE id=?", (selected_id,))
                conn.commit()
                st.warning("Data berhasil dihapus")
                st.rerun()

        # ======================
        # DELETE ALL
        # ======================
        st.divider()
        st.subheader("⚠️ Hapus Semua Data")

        confirm = st.text_input("Ketik 'HAPUS' untuk konfirmasi")

        if confirm == "HAPUS":
            if st.button("🗑️ Hapus Semua", use_container_width=True):

                conn.execute("""
                    DELETE FROM akun_nusuk 
                    WHERE user_id=? AND gender=?
                """, (user["id"], gender))

                conn.commit()
                st.success("Semua data terhapus ✅")
                st.rerun()
