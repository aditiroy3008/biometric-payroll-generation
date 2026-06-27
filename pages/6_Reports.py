import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO
from utils.header import show_header

show_header()

DB_PATH = "data/workforce.db"

st.title("📄 Reports & Exports")

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

conn.close()
st.subheader("👷 Employee Master")

st.dataframe(
    employees,
    use_container_width=True
)

employee_buffer = BytesIO()

with pd.ExcelWriter(
    employee_buffer,
    engine="openpyxl"
) as writer:

    employees.to_excel(
        writer,
        index=False,
        sheet_name="Employee_Master"
    )

st.download_button(
    "📥 Download Employee Master",
    data=employee_buffer.getvalue(),
    file_name="employee_master.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
st.divider()

st.subheader("🕒 Attendance Register")

st.dataframe(
    attendance,
    use_container_width=True
)

attendance_buffer = BytesIO()

with pd.ExcelWriter(
    attendance_buffer,
    engine="openpyxl"
) as writer:

    attendance.to_excel(
        writer,
        index=False,
        sheet_name="Attendance"
    )

st.download_button(
    "📥 Download Attendance Register",
    data=attendance_buffer.getvalue(),
    file_name="attendance_register.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
st.divider()

st.subheader("💰 Payroll Register")

if not attendance.empty:

    rates = pd.read_sql(
        "SELECT * FROM category_rates",
        sqlite3.connect(DB_PATH)
    )

    payroll_data = []

    attendance["date"] = pd.to_datetime(
        attendance["date"]
    )

    latest_month = (
        attendance["date"]
        .dt.strftime("%Y-%m")
        .max()
    )

    month_data = attendance[
        attendance["date"]
        .dt.strftime("%Y-%m")
        == latest_month
    ]

    for _, emp in employees.iterrows():

        emp_att = month_data[
            month_data["employee_id"]
            == emp["employee_id"]
        ]

        total_hours = emp_att[
            "working_hours"
        ].sum()

        total_ot = emp_att[
            "ot_hours"
        ].sum()

        rate_row = rates[
            rates["category"]
            == emp["category"]
        ].iloc[0]

        hourly_rate = rate_row[
            "hourly_rate"
        ]

        ot_multiplier = rate_row[
            "ot_multiplier"
        ]

        salary = (
            total_hours * hourly_rate
        ) + (
            total_ot *
            hourly_rate *
            ot_multiplier
        )

        payroll_data.append({
            "Employee ID":
            emp["employee_id"],

            "Worker":
            emp["worker_name"],

            "Category":
            emp["category"],

            "Hours":
            total_hours,

            "OT":
            total_ot,

            "Salary":
            round(salary, 2)
        })

    payroll_df = pd.DataFrame(
        payroll_data
    )

    st.dataframe(
        payroll_df,
        use_container_width=True
    )

    payroll_buffer = BytesIO()

    with pd.ExcelWriter(
        payroll_buffer,
        engine="openpyxl"
    ) as writer:

        payroll_df.to_excel(
            writer,
            index=False,
            sheet_name="Payroll"
        )

    st.download_button(
        "📥 Download Payroll Register",
        data=payroll_buffer.getvalue(),
        file_name="payroll_register.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:

    st.info(
        "No attendance records available."
    )