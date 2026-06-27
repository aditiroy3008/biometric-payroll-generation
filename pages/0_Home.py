import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import date
from utils.header import show_header

show_header()

DB_PATH = "data/workforce.db"

# =====================================================
# LOAD DATA
# =====================================================

conn = sqlite3.connect(DB_PATH)

employees = pd.read_sql(
    "SELECT * FROM employees",
    conn
)

attendance = pd.read_sql(
    "SELECT * FROM attendance",
    conn
)

conn.close()

# =====================================================
# KPI DATA
# =====================================================

total_workers = len(employees)

active_workers = len(
    employees[
        employees["status"] == "Active"
    ]
)

today_attendance = len(
    attendance[
        attendance["date"] == str(date.today())
    ]
)

contractors = (
    employees["contractor_name"].nunique()
    if not employees.empty
    else 0
)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
# ITC Workforce Management System

Contract Labour Attendance, Payroll & Biometric Automation Platform
""")

st.divider()

# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Workers",
        total_workers
    )

with col2:
    st.metric(
        "Active Workers",
        active_workers
    )

with col3:
    st.metric(
        "Today's Attendance",
        today_attendance
    )

with col4:
    st.metric(
        "Contractors",
        contractors
    )

st.divider()

# =====================================================
# CHARTS
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Workforce Distribution")

    if not employees.empty:

        category_df = (
            employees["category"]
            .value_counts()
            .reset_index()
        )

        category_df.columns = [
            "Category",
            "Workers"
        ]

        fig = px.pie(
            category_df,
            names="Category",
            values="Workers",
            hole=0.55
        )

        fig.update_layout(
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with col2:

    st.subheader("Contractor Distribution")

    if not employees.empty:

        contractor_df = (
            employees["contractor_name"]
            .value_counts()
            .reset_index()
        )

        contractor_df.columns = [
            "Contractor",
            "Workers"
        ]

        fig = px.bar(
            contractor_df,
            x="Contractor",
            y="Workers"
        )

        fig.update_layout(
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# =====================================================
# SYSTEM OVERVIEW
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Modules Available")

    st.write("• Employee Master Management")
    st.write("• Attendance Management")
    st.write("• Payroll Processing")
    st.write("• Category Rate Management")
    st.write("• Biometric Integration")

with col2:

    st.subheader("System Status")

    st.success("Database Connected")
    st.success("Attendance Module Active")
    st.success("Payroll Module Active")
    st.success("Reporting Module Active")
    st.success("Biometric Ready")

st.divider()

# =====================================================
# RECENT ATTENDANCE
# =====================================================

st.subheader("Recent Attendance")

if not attendance.empty:

    recent_df = attendance.sort_values(
        by="attendance_id",
        ascending=False
    ).head(10)

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No attendance records available."
    )