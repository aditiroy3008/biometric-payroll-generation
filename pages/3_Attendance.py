import streamlit as st
import sqlite3
import pandas as pd
from utils.header import show_header

show_header()
DB_PATH = "data/workforce.db"

st.title("🕒 Attendance Management")

# =====================================
# LOAD ATTENDANCE
# =====================================

conn = sqlite3.connect(DB_PATH)

attendance_df = pd.read_sql("""
SELECT *
FROM attendance
ORDER BY attendance_id DESC
""", conn)

conn.close()

# =====================================
# METRICS
# =====================================

st.subheader("Attendance Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Attendance Records",
        len(attendance_df)
    )

with col2:

    total_hours = (
        round(
            attendance_df["working_hours"].sum(),
            2
        )
        if not attendance_df.empty
        else 0
    )

    st.metric(
        "Total Hours",
        total_hours
    )

with col3:

    total_ot = (
        round(
            attendance_df["ot_hours"].sum(),
            2
        )
        if not attendance_df.empty
        else 0
    )

    st.metric(
        "OT Hours",
        total_ot
    )

# =====================================
# REGISTER
# =====================================

st.divider()

st.subheader("📋 Attendance Register")

if attendance_df.empty:

    st.info(
        "No attendance records available."
    )

else:

    st.dataframe(
        attendance_df,
        use_container_width=True,
        hide_index=True
    )

# =====================================
# DELETE RECORD
# =====================================

st.divider()

st.subheader("🗑 Delete Attendance Record")

if not attendance_df.empty:

    selected_record = st.selectbox(
        "Select Attendance ID",
        attendance_df["attendance_id"]
    )

    if st.button("Delete Selected Record"):

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM attendance
        WHERE attendance_id=?
        """,
        (int(selected_record),)
        )

        conn.commit()
        conn.close()

        st.success(
            "Attendance record deleted."
        )

        st.rerun()

# =====================================
# DELETE ALL
# =====================================

st.divider()

if st.button(
    "🗑 Delete All Attendance Records"
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM attendance"
    )

    conn.commit()
    conn.close()

    st.success(
        "All attendance records deleted."
    )

    st.rerun()