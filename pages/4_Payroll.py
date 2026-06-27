import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO
import utils.header

utils.header.show_header()

DB_PATH = "data/workforce.db"

st.title("💰 Payroll Management")

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

if attendance.empty:
    st.warning("No attendance records found.")
    st.stop()

# =====================================
# MONTH SELECTION
# =====================================

attendance["date"] = pd.to_datetime(
    attendance["date"]
)

available_months = sorted(
    attendance["date"]
    .dt.strftime("%Y-%m")
    .unique(),
    reverse=True
)

selected_month = st.selectbox(
    "Select Payroll Month",
    available_months
)

# =====================================
# FILTER MONTH
# =====================================

attendance_month = attendance[
    attendance["date"]
    .dt.strftime("%Y-%m")
    == selected_month
]

# =====================================
# PAYROLL GENERATION
# =====================================

if st.button("Generate Payroll"):

    payroll_data = []

    for _, emp in employees.iterrows():

        emp_attendance = attendance_month[
            attendance_month["employee_id"]
            == emp["employee_id"]
        ]

        total_hours = emp_attendance[
            "working_hours"
        ].sum()

        total_ot_hours = emp_attendance[
            "ot_hours"
        ].sum()

        category_rate = rates[
            rates["category"]
            == emp["category"]
        ].iloc[0]

        hourly_rate = category_rate[
            "hourly_rate"
        ]

        ot_multiplier = category_rate[
            "ot_multiplier"
        ]

        normal_pay = (
            total_hours *
            hourly_rate
        )

        ot_pay = (
            total_ot_hours *
            hourly_rate *
            ot_multiplier
        )

        total_salary = (
            normal_pay +
            ot_pay
        )

        payroll_data.append({

            "Employee ID":
            emp["employee_id"],

            "Worker Name":
            emp["worker_name"],

            "Contractor":
            emp["contractor_name"],

            "Category":
            emp["category"],

            "Hours Worked":
            round(total_hours, 2),

            "OT Hours":
            round(total_ot_hours, 2),

            "Hourly Rate":
            hourly_rate,

            "Normal Pay":
            round(normal_pay, 2),

            "OT Pay":
            round(ot_pay, 2),

            "Total Salary":
            round(total_salary, 2)

        })

    payroll_df = pd.DataFrame(
        payroll_data
    )

    # =====================================
    # SUMMARY METRICS
    # =====================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Workers",
            len(payroll_df)
        )

    with col2:
        st.metric(
            "Total Hours",
            round(
                payroll_df[
                    "Hours Worked"
                ].sum(),
                2
            )
        )

    with col3:
        st.metric(
            "Total Payroll",
            f"₹ {round(payroll_df['Total Salary'].sum(),2):,.2f}"
        )

    st.divider()

    # =====================================
    # TABLE
    # =====================================

    st.subheader(
        f"Payroll Register - {selected_month}"
    )

    st.dataframe(
        payroll_df,
        use_container_width=True,
        hide_index=True
    )

    # =====================================
    # EXCEL EXPORT
    # =====================================

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        payroll_df.to_excel(
            writer,
            index=False,
            sheet_name="Payroll"
        )

    st.download_button(
        "📥 Download Payroll Register",
        data=output.getvalue(),
        file_name=f"payroll_{selected_month}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )