import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import requests


@st.cache_resource
def connect_to_sheets():
    try:
        credentials_dict = dict(st.secrets["google_credentials"])
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_info(credentials_dict, scopes=scope)
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Google Sheets connection error: {e}")
        return None


@st.cache_data(ttl=300)
def load_cora_data():
    try:
        client = connect_to_sheets()
        sheet = client.open_by_key(st.secrets["CORA_SHEET_ID"]).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=120)
def load_opsi_data():
    try:
        client = connect_to_sheets()
        sheet = client.open_by_key(st.secrets["OPSI_SHEET_ID"]).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame()


def send_opsi_task(task_data):
    webhook_url = "https://hackett2k.app.n8n.cloud/webhook/opsi-create-task"
    try:
        response = requests.post(webhook_url, json=task_data)
        return response.json()
    except Exception as e:
        st.error(f"Task creation error: {e}")
        return None
