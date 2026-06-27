import streamlit as st
import sqlite3
import pandas as pd
from utils.header import show_header

show_header()

DB_PATH = "data/workforce.db"

st.title("💰 Category Rate Management")

# Load Rates

conn = sqlite3.connect(DB_PATH)

rates_df = pd.read_sql(
    "SELECT * FROM category_rates",
    conn
)

conn.close()

st.subheader("Current Rates")

edited_df = st.data_editor(
    rates_df,
    use_container_width=True,
    num_rows="fixed"
)

# Save Changes

if st.button("💾 Save Changes"):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM category_rates"
    )

    for _, row in edited_df.iterrows():

        cursor.execute("""
        INSERT INTO category_rates
        VALUES (?, ?, ?)
        """,
        (
            row["category"],
            row["hourly_rate"],
            row["ot_multiplier"]
        ))

    conn.commit()
    conn.close()

    st.success(
        "Category rates updated successfully."
    )

    st.rerun()