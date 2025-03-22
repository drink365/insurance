import streamlit as st
import pandas as pd
import sqlite3

# 標題
st.title("保險商品推薦平台")

# 連接 SQLite 數據庫
conn = sqlite3.connect('insurance.db')

# 查詢保險商品數據
query = "SELECT * FROM insurance_products"
df = pd.read_sql_query(query, conn)

# 顯示數據
st.write("保險商品列表：")
st.dataframe(df)

# 關閉數據庫連接
conn.close()
