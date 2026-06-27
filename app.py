import streamlit as st
import database


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="ITC Workforce Management",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# GLOBAL CSS
# =====================================

st.markdown("""
<style>

/* Background */
.stApp{
    background-color:#F8F6F3;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:white;
    border-right:1px solid #E5E5E5;
}

section[data-testid="stSidebar"] *{
    color:#1F2A44 !important;
}

/* Headings */
h1,h2,h3{
    color:#6D0019;
    font-weight:700;
}

/* Buttons */
.stButton button{
    background:#6D0019;
    color:white;
    border:none;
    border-radius:12px;
    padding:0.5rem 1rem;
    font-weight:600;
}

.stButton button:hover{
    background:#520014;
}

/* Inputs */
.stTextInput input,
.stSelectbox,
.stDateInput,
.stTimeInput{
    border-radius:10px !important;
}

/* DataFrames */
[data-testid="stDataFrame"]{
    border-radius:15px;
    overflow:hidden;
}

/* Metric Cards */
.metric-card{
    background:white;
    padding:25px;
    border-radius:18px;
    border-top:5px solid #A67C52;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
}

.metric-title{
    color:#6D0019;
    font-size:16px;
    font-weight:600;
}

.metric-value{
    color:#2B2B2B;
    font-size:34px;
    font-weight:bold;
}

/* Success */
[data-testid="stAlert"]{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR BRANDING
# =====================================

with st.sidebar:

    try:
        st.image(
            "assets/itc_logo.png",
            width=150
        )
    except:
        pass

    st.markdown("""
    ## ITC Workforce

    Contract Labour Attendance,
    Payroll & Biometric Automation
    """)

    st.divider()

# =====================================
# HOME SCREEN
# =====================================

st.markdown("""
<div style="
padding:50px;
border-radius:20px;
background:linear-gradient(135deg,#EAF4FF,#CFE7FF);
color:#1F2A44;
text-align:center;
">
<h1>🏭 ITC Workforce Management System</h1>

<h3>
Contract Labour Attendance, Payroll &
Biometric Integration Platform
</h3>

<p>
Future Ready for Fingerprint, Facial Recognition
and Smart Attendance Systems
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

st.markdown("""
<div style="
background:#F5F9FF;
padding:20px;
border-radius:15px;
border-left:5px solid #A67C52;
color:#1F2A44;
">
Use the navigation menu on the left to manage Employees,
Attendance, Payroll, Dashboard, Reports and Biometric Integration.
</div>
""", unsafe_allow_html=True)