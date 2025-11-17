import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .status-active {
            background:#10b981;
            padding:4px 8px;
            border-radius:4px;
            color:white;
        }
        .status-idle {
            background:#f59e0b;
            padding:4px 8px;
            border-radius:4px;
            color:white;
        }
    </style>
    """, unsafe_allow_html=True)

