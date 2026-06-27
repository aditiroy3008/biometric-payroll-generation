import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO
from utils.header import show_header

show_header()

DB_PATH = "data/workforce.db"

st.title("👷 Employee Master")

# =====================================================
# ADD WORKER
# =====================================================

st.subheader("Add New Worker")

with st.form("employee_form"):

    col1, col2 = st.columns(2)

    with col1:

        employee_id = st.text_input(
            "Employee ID *",
            placeholder="EMP001"
        )

        biometric_id = st.text_input(
            "Biometric ID *",
            placeholder="BIO001"
        )

        worker_name = st.text_input(
            "Worker Name *",
            placeholder="Rahul Kumar"
        )

    with col2:

        contractor_name = st.text_input(
            "Contractor Name *",
            placeholder="ABC Contractors"
        )

        category = st.selectbox(
            "Category *",
            [
                "Unskilled",
                "Semi-Skilled",
                "Skilled",
                "High-Skilled"
            ]
        )

        status = st.selectbox(
            "Status *",
            [
                "Active",
                "Inactive"
            ]
        )

    submit = st.form_submit_button(
        "Add Worker"
    )

    if submit:

        if (
            employee_id.strip() == ""
            or biometric_id.strip() == ""
            or worker_name.strip() == ""
            or contractor_name.strip() == ""
        ):

            st.error(
                "⚠️ All fields are mandatory."
            )

        else:

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            try:

                cursor.execute("""
                INSERT INTO employees
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    employee_id,
                    biometric_id,
                    worker_name,
                    contractor_name,
                    category,
                    status
                ))

                conn.commit()

                st.success(
                    f"✅ {worker_name} added successfully."
                )

            except sqlite3.IntegrityError:

                st.error(
                    "⚠️ Employee ID or Biometric ID already exists."
                )

            conn.close()

# =====================================================
# LOAD DATA
# =====================================================

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(
    "SELECT * FROM employees",
    conn
)

conn.close()

# =====================================================
# SEARCH
# =====================================================

st.divider()

st.subheader("🔍 Search Worker")

search = st.text_input(
    "Search by Employee ID, Biometric ID or Name"
)

filtered_df = df.copy()

if search:

    filtered_df = filtered_df[
        filtered_df["employee_id"].str.contains(
            search,
            case=False,
            na=False
        )
        |
        filtered_df["biometric_id"].str.contains(
            search,
            case=False,
            na=False
        )
        |
        filtered_df["worker_name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]
# =====================================
# KPI DATA
# =====================================

total_workers = len(df)

active_workers = len(
    df[df["status"] == "Active"]
)

inactive_workers = len(
    df[df["status"] == "Inactive"]
)

contractors = df["contractor_name"].nunique()
# =====================================================
# METRICS
# =====================================================

st.markdown("""
<style>
.metric-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
    border-left:5px solid #A67C52;
    margin-bottom:10px;
}

.metric-title{
    color:#6D0019;
    font-size:16px;
    font-weight:600;
}

.metric-value{
    color:#2B2B2B;
    font-size:32px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">👷 Total Workers</div>
        <div class="metric-value">{total_workers}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">✅ Active Workers</div>
        <div class="metric-value">{active_workers}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">⛔ Inactive Workers</div>
        <div class="metric-value">{inactive_workers}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🏢 Contractors</div>
        <div class="metric-value">{contractors}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.subheader("📤 Bulk Employee Upload")


# =====================================
# TEMPLATE DOWNLOAD
# =====================================

st.subheader("Employee Template")

template_df = pd.DataFrame({
    "employee_id": ["EMP001"],
    "biometric_id": ["BIO001"],
    "worker_name": ["Rahul Kumar"],
    "contractor_name": ["ABC Contractors"],
    "category": ["Skilled"],
    "status": ["Active"]
})

buffer = BytesIO()

with pd.ExcelWriter(
    buffer,
    engine="openpyxl"
) as writer:

    template_df.to_excel(
        writer,
        index=False,
        sheet_name="Employees"
    )

    # Category reference sheet
    pd.DataFrame({
        "Allowed Categories": [
            "Unskilled",
            "Semi-Skilled",
            "Skilled",
            "High-Skilled"
        ]
    }).to_excel(
        writer,
        index=False,
        sheet_name="Categories"
    )

    # Status reference sheet
    pd.DataFrame({
        "Allowed Status": [
            "Active",
            "Inactive"
        ]
    }).to_excel(
        writer,
        index=False,
        sheet_name="Status"
    )

st.download_button(
    label="📥 Download Employee Template",
    data=buffer.getvalue(),
    file_name="employee_template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =====================================================
# EMPLOYEE ACTIONS
# =====================================================

st.divider()

st.subheader("⚙️ Employee Actions")

if not df.empty:

    selected_emp = st.selectbox(
        "Select Employee",
        df["employee_id"]
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("⛔ Deactivate Employee"):

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("""
            UPDATE employees
            SET status='Inactive'
            WHERE employee_id=?
            """,
            (selected_emp,)
            )

            conn.commit()
            conn.close()

            st.success(
                f"{selected_emp} deactivated."
            )

            st.rerun()

    with col2:

        if st.button("🗑 Delete Employee"):

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("""
            DELETE FROM employees
            WHERE employee_id=?
            """,
            (selected_emp,)
            )

            conn.commit()
            conn.close()

            st.success(
                f"{selected_emp} deleted."
            )

            st.rerun()

# =====================================================
# EDIT EMPLOYEE
# =====================================================

st.divider()

st.subheader("✏️ Edit Employee")

if not df.empty:

    edit_emp = st.selectbox(
        "Choose Employee To Edit",
        df["employee_id"],
        key="edit_employee"
    )

    emp = df[
        df["employee_id"] == edit_emp
    ].iloc[0]

    with st.form("edit_form"):

        new_name = st.text_input(
            "Worker Name",
            value=emp["worker_name"]
        )

        new_contractor = st.text_input(
            "Contractor Name",
            value=emp["contractor_name"]
        )

        category_list = [
            "Unskilled",
            "Semi-Skilled",
            "Skilled",
            "High-Skilled"
        ]

        # Fix old values like SKILLED
        category_mapping = {
            "UNSKILLED": "Unskilled",
            "SEMI-SKILLED": "Semi-Skilled",
            "SKILLED": "Skilled",
            "HIGH-SKILLED": "High-Skilled"
        }

        current_category = category_mapping.get(
            str(emp["category"]).strip().upper(),
            "Unskilled"
        )

        new_category = st.selectbox(
            "Category",
            category_list,
            index=category_list.index(current_category)
        )

        new_status = st.selectbox(
            "Status",
            ["Active", "Inactive"],
            index=0 if emp["status"] == "Active" else 1
        )

        update_btn = st.form_submit_button(
            "Update Employee"
        )

        if update_btn:

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("""
            UPDATE employees
            SET worker_name=?,
                contractor_name=?,
                category=?,
                status=?
            WHERE employee_id=?
            """,
            (
                new_name,
                new_contractor,
                new_category,
                new_status,
                edit_emp
            ))

            conn.commit()
            conn.close()

            st.success(
                "✅ Employee Updated Successfully"
            )

            st.rerun()