import streamlit as st
import pandas as pd

st.title('💰 保單試算平台 - 直接讀取 Google Sheets')

# **Google Sheets CSV 下載連結**
gdrive_url = "https://docs.google.com/spreadsheets/d/1ITlpwQNV29tWOqcNoTHRq9R3iENoPisp/export?format=csv"

@st.cache_data
def load_google_sheets(url):
    return pd.read_csv(url)

try:
    # **讀取 Google Sheets 資料**
    df = load_google_sheets(gdrive_url)

    # **顯示 Google Sheets 資料**
    st.write("📋 **Google Sheets 資料預覽**")
    st.dataframe(df.head())

    st.info("✅ 成功讀取 Google Sheets 資料！請確保資料格式正確。")

except Exception as e:
    st.error("❌ 無法讀取 Google Sheets，請檢查權限是否正確！")
    st.text(str(e))
