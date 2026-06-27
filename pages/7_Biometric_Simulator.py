import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
from utils.header import show_header

show_header()

DB_PATH = "data/workforce.db"

st.title("🔐 Biometric Simulator")

st.info(
    "Simulates biometric attendance using Biometric ID."
)

biometric_id = st.text_input(
    "Enter Biometric ID",
    placeholder="BIO001"
)

if st.button("Scan"):

    if biometric_id.strip() == "":

        st.error(
            "Please enter a Biometric ID."
        )

    else:

        conn = sqlite3.connect(DB_PATH)

        employee = pd.read_sql(
            """
            SELECT *
            FROM employees
            WHERE biometric_id=?
            """,
            conn,
            params=(biometric_id,)
        )

        if employee.empty:

            st.error(
                "Biometric ID not found."
            )

        else:

            emp = employee.iloc[0]

            st.success(
                f"Worker Found: {emp['worker_name']}"
            )

            today = str(date.today())

            current_time = datetime.now().strftime(
                "%H:%M:%S"
            )

            attendance = pd.read_sql(
                """
                SELECT *
                FROM attendance
                WHERE employee_id=?
                AND date=?
                ORDER BY attendance_id DESC
                LIMIT 1
                """,
                conn,
                params=(
                    emp["employee_id"],
                    today
                )
            )

            cursor = conn.cursor()

            # =====================================
            # FIRST SCAN = CHECK IN
            # =====================================

            if attendance.empty:

                cursor.execute("""
                INSERT INTO attendance
                (
                    employee_id,
                    biometric_id,
                    date,
                    check_in,
                    check_out,
                    working_hours,
                    ot_hours,
                    source
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    emp["employee_id"],
                    biometric_id,
                    today,
                    current_time,
                    "",
                    0,
                    0,
                    "Biometric"
                ))

                conn.commit()

                st.success(
                    f"✅ Check-In Recorded at {current_time}"
                )

            else:

                row = attendance.iloc[0]

                # =====================================
                # SECOND SCAN = CHECK OUT
                # =====================================

                if (
                    pd.isna(row["check_out"])
                    or str(row["check_out"]).strip() == ""
                ):

                    check_in_time = row["check_in"]

                    in_dt = datetime.strptime(
                        f"{today} {check_in_time}",
                        "%Y-%m-%d %H:%M:%S"
                    )

                    out_dt = datetime.strptime(
                        f"{today} {current_time}",
                        "%Y-%m-%d %H:%M:%S"
                    )

                    working_hours = round(
                        (
                            out_dt - in_dt
                        ).total_seconds() / 3600,
                        2
                    )

                    ot_hours = max(
                        0,
                        round(
                            working_hours - 8,
                            2
                        )
                    )

                    cursor.execute("""
                    UPDATE attendance
                    SET check_out=?,
                        working_hours=?,
                        ot_hours=?
                    WHERE attendance_id=?
                    """,
                    (
                        current_time,
                        working_hours,
                        ot_hours,
                        int(row["attendance_id"])
                    ))

                    conn.commit()

                    st.success(
                        f"✅ Check-Out Recorded at {current_time}"
                    )

                    st.info(
                        f"""
Working Hours: {working_hours}

OT Hours: {ot_hours}
"""
                    )

                else:

                    st.warning(
                        "Attendance already completed for today."
                    )

        conn.close()

st.divider()

conn = sqlite3.connect(DB_PATH)

log_df = pd.read_sql(
    """
    SELECT *
    FROM attendance
    ORDER BY attendance_id DESC
    """,
    conn
)

conn.close()

st.subheader("📋 Attendance Log")

st.dataframe(
    log_df,
    use_container_width=True,
    hide_index=True
)