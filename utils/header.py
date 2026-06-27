import streamlit as st

def show_header():

    col1, col2 = st.columns([1, 8])

    with col1:
        st.image(
            "assets/itc_logo.png",
            width=90
        )

    with col2:
        st.markdown("""
        <h2 style="
        color:#1E293B;
        margin-top:15px;
        ">
        ITC Workforce Management System
        </h2>
        """, unsafe_allow_html=True)

    st.divider()