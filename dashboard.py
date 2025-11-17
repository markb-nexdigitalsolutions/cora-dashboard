import streamlit as st
from datetime import datetime

from cora import cora_page
from mark import mark_page
from opsi import opsi_page
from utils import load_cora_data, load_opsi_data
from styles import load_css


# ----------------------------------------------------
# STREAMLIT SETUP + GLOBAL STYLE
# ----------------------------------------------------
st.set_page_config(
    page_title="ApexxAdams Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()   # Load global CSS


# ----------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------
st.sidebar.title("Agent Control Panel")
st.sidebar.markdown("---")

st.sidebar.subheader("Agent Status")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.markdown('<span class="status-active">CORA</span>', unsafe_allow_html=True)
with col2:
    st.markdown('<span class="status-idle">MARK</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="status-active">OPSI</span>', unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Select Agent",
    ["Dashboard Overview", "CORA (Lead Generation)", "MARK (Marketing AI)", "OPSI (Operations)"]
)

st.sidebar.markdown("---")

# Quick triggers
if st.sidebar.button("Run CORA Now"):
    st.sidebar.success("CORA workflow triggered!")

if st.sidebar.button("Ask MARK"):
    st.sidebar.info("Opening MARK...")

if st.sidebar.button("View OPSI Tasks"):
    st.sidebar.info("Loading OPSI tasks...")


# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown('<h1 class="main-header">ApexxAdams Command Center</h1>', unsafe_allow_html=True)
st.write("Multi-Agent System Dashboard - CORA | MARK | OPSI")
st.markdown("---")


# ----------------------------------------------------
# PAGE ROUTING
# ----------------------------------------------------
if page == "Dashboard Overview":

    cora_df = load_cora_data()
    opsi_df = load_opsi_data()

    st.subheader("System Overview")

    import pandas as pd
    status_col = "Status " if "Status " in opsi_df.columns else "Status"
    priority_col = "Priority " if "Priority " in opsi_df.columns else "Priority"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        pending = len(opsi_df[opsi_df[status_col] == "New"]) if not opsi_df.empty else 0
        st.metric("Pending Tasks", pending)

    with col2:
        in_progress = len(opsi_df[opsi_df[status_col] == "In Progress"]) if not opsi_df.empty else 0
        st.metric("In Progress", in_progress)

    with col3:
        high = len(opsi_df[opsi_df[priority_col] == "High"]) if not opsi_df.empty else 0
        st.metric("High Priority", high)

    with col4:
        st.metric("Overall Performance", "68%" if not cora_df.empty else "N/A")

    st.markdown("---")

    colA, colB = st.columns(2)

    with colA:
        st.subheader("Latest CORA Leads")
        if not cora_df.empty:
            subset = cora_df.tail(5)
            st.dataframe(subset, use_container_width=True, hide_index=True)
        else:
            st.info("No CORA leads available.")

    with colB:
        st.subheader("Upcoming OPSI Tasks")
        if not opsi_df.empty:
            subset = opsi_df.head(5)
            st.dataframe(subset, use_container_width=True, hide_index=True)
        else:
            st.info("No OPSI tasks available.")

elif page == "CORA (Lead Generation)":
    cora_page()

elif page == "MARK (Marketing AI)":
    mark_page()

elif page == "OPSI (Operations)":
    opsi_page()


# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align:center; color:#666; padding:1rem;'>
        <strong>ApexxAdams Multi-Agent Command Center</strong><br>
        Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    </div>
    """,
    unsafe_allow_html=True
)
