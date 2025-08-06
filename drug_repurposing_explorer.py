
import streamlit as st
import pandas as pd
import sqlite3
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Drug Repurposing DB Explorer", layout="wide")
st.title("🧬 Drug Repurposing Explorer for PCOS and Endometrial Cancer")

# --- FILE MAPPING ---
xls_mapping = {
    "geo_pcos": "pone.0271380.s001.xls",
    "geo_endometrial": "pone.0271380.s002.xls",
    "ppi_network": "pone.0271380.s003.xls",
    "tf_regulators": "pone.0271380.s004.xls",
    "mirna_regulators": "pone.0271380.s005.xls",
    "drug_candidates": "pone.0271380.s006.xls"
}

db_path = "drug_repurposing.db"
loaded_tables = []

# --- DATABASE CREATION ---
if not os.path.exists(db_path):
    st.info("🔧 Creating local database from Excel files...")
    conn = sqlite3.connect(db_path)

    for table_key, filename in xls_mapping.items():
        try:
            df = pd.read_excel(filename)
            table_name = table_key.lower()
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            loaded_tables.append((filename, table_name))
            st.success(f"✅ Loaded: {table_name}")
        except Exception as e:
            st.error(f"❌ Error loading {filename}: {e}")

    conn.commit()
    conn.close()
    st.success("🎉 Database created successfully!")

# --- SIDEBAR INFO ---
with st.sidebar:
    st.markdown("### 📊 Tables Included:")
    for name, file in xls_mapping.items():
        st.markdown(f"- **{name}** ({file})")

# --- SQL QUERY INTERFACE ---
st.markdown("### 💻 Run SQL Query")

query = st.text_area(
    "Enter your SQL query below:",
    value="SELECT name FROM sqlite_master WHERE type='table';",
    height=200
)

if st.button("Run Query"):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        st.success("✅ Query successful!")
        st.dataframe(df)
    except Exception as e:
        st.error(f"❌ SQL Error: {e}")
