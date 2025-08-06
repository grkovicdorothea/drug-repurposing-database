import streamlit as st
import pandas as pd
import sqlite3
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Drug Repurposing Database Explorer", layout="wide")
st.title("Drug Repurposing for Women's Health Database")

# --- FILE MAPPING ---
csv_mapping = {
    "geo_pcos": "pone.0271380.s001.csv",
    "geo_endometrial": "pone.0271380.s002.csv",
    "ppi_network": "pone.0271380.s003.csv",
    "tf_regulators": "pone.0271380.s004.csv",
    "mirna_regulators": "pone.0271380.s005.csv",
    "drug_candidates": "pone.0271380.s006.csv"
}

db_path = "drug_repurposing.db"
loaded_tables = []

# --- DATABASE CREATION ---
if not os.path.exists(db_path):
    st.info("🔧 Creating local database from CSV files...")
    conn = sqlite3.connect(db_path)

    for table_key, filename in csv_mapping.items():
        try:
            df = pd.read_csv(filename)
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
# --- SIDEBAR INFO ---
with st.sidebar:
    st.markdown("### Tables Included with Headers:")
    for table_key, filename in csv_mapping.items():
        st.markdown(f"**{table_key}** ({filename})")
        try:
            df = pd.read_csv(filename, nrows=0)  # read only headers
            headers = df.columns.tolist()
            st.markdown(", ".join(headers))
        except Exception as e:
            st.error(f"❌ Error reading {filename}: {e}")

# --- SQL QUERY INTERFACE ---
st.markdown("### Run SQL Query")

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
