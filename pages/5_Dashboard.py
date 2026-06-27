import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from utils.header import show_header

show_header()
DB_PATH = "data/workforce.db"

st.title("📊 Workforce Dashboard")

# =====================================
# LOAD DATA
# =====================================

conn = sqlite3.connect(DB_PATH)

employees = pd.read_sql(
    "SELECT * FROM employees",
    conn
)

attendance = pd.read_sql(
    "SELECT * FROM attendance",
    conn
)

rates = pd.read_sql(
    "SELECT * FROM category_rates",
    conn
)

conn.close()

# =====================================
# KPI CARDS
# =====================================

total_workers = len(employees)

active_workers = len(
    employees[
        employees["status"] == "Active"
    ]
)

total_hours = (
    round(attendance["working_hours"].sum(), 2)
    if not attendance.empty
    else 0
)

# Payroll Estimate

estimated_payroll = 0

if (
    not employees.empty
    and not attendance.empty
):

    attendance_summary = (
        attendance
        .groupby("employee_id")
        [["working_hours", "ot_hours"]]
        .sum()
        .reset_index()
    )

    payroll_df = attendance_summary.merge(
        employees,
        on="employee_id"
    )

    payroll_df = payroll_df.merge(
        rates,
        on="category"
    )

    payroll_df["salary"] = (
        payroll_df["working_hours"]
        * payroll_df["hourly_rate"]
        +
        payroll_df["ot_hours"]
        * payroll_df["hourly_rate"]
        * payroll_df["ot_multiplier"]
    )

    estimated_payroll = round(
        payroll_df["salary"].sum(),
        2
    )

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
        "Total Hours",
        total_hours
    )

with col4:
    st.metric(
        "Payroll Cost",
        f"₹ {estimated_payroll:,.0f}"
    )

st.divider()

# =====================================
# CATEGORY DISTRIBUTION
# =====================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Category-wise Workforce")

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
        values="Workers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("Contractor-wise Workforce")

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

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# ATTENDANCE TREND
# =====================================

st.subheader("Attendance Trend")

if not attendance.empty:

    trend_df = (
        attendance
        .groupby("date")
        .size()
        .reset_index(name="Records")
    )

    fig = px.line(
        trend_df,
        x="date",
        y="Records",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No attendance data available."
    )

# =====================================
# TOP WORKERS BY HOURS
# =====================================

st.subheader("Top Workers by Hours")

if not attendance.empty:

    worker_hours = (
        attendance
        .groupby("employee_id")
        ["working_hours"]
        .sum()
        .reset_index()
    )

    worker_hours = worker_hours.merge(
        employees[
            ["employee_id", "worker_name"]
        ],
        on="employee_id"
    )

    worker_hours = worker_hours.sort_values(
        by="working_hours",
        ascending=False
    )

    st.dataframe(
        worker_hours,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No attendance records available."
    )