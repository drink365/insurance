import streamlit as st
import pandas as pd
import os

# 定義 CSV 檔案儲存路徑
DATA_FILE = 'insurance_products.csv'

# 載入資料，如果檔案不存在則建立一個空的 DataFrame 並存檔
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["ID", "Name", "Description", "Price"])
        df.to_csv(DATA_FILE, index=False)
    return df

# 儲存資料到 CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Streamlit 介面
st.title("保險商品管理系統")
st.write("請利用側邊選單來選擇操作功能：新增、修改、刪除或檢視所有商品。")

# 載入現有資料
df = load_data()

# 側邊選單
menu = ["新增", "修改", "刪除", "查看所有"]
choice = st.sidebar.selectbox("選擇操作", menu)

if choice == "新增":
    st.subheader("新增保險商品")
    new_id = st.text_input("商品ID")
    new_name = st.text_input("商品名稱")
    new_desc = st.text_area("商品描述")
    new_price = st.number_input("價格", min_value=0.0, step=0.1)
    
    if st.button("新增商品"):
        if new_id and new_name:
            # 檢查 ID 是否已存在
            if new_id in df["ID"].values:
                st.error("商品ID已存在，請使用不同的ID。")
            else:
                new_data = {"ID": new_id, "Name": new_name, "Description": new_desc, "Price": new_price}
                df = df.append(new_data, ignore_index=True)
                save_data(df)
                st.success("成功新增商品！")
        else:
            st.error("請填入必填欄位：商品ID 與 商品名稱。")
                
elif choice == "修改":
    st.subheader("修改保險商品")
    if df.empty:
        st.warning("目前沒有資料可以修改。")
    else:
        selected_id = st.selectbox("選擇要修改的商品ID", df["ID"].tolist())
        product = df[df["ID"] == selected_id].iloc[0]
        
        new_name = st.text_input("商品名稱", value=product["Name"])
        new_desc = st.text_area("商品描述", value=product["Description"])
        new_price = st.number_input("價格", value=float(product["Price"]), step=0.1)
        
        if st.button("儲存修改"):
            df.loc[df["ID"] == selected_id, "Name"] = new_name
            df.loc[df["ID"] == selected_id, "Description"] = new_desc
            df.loc[df["ID"] == selected_id, "Price"] = new_price
            save_data(df)
            st.success("成功修改商品！")
        
elif choice == "刪除":
    st.subheader("刪除保險商品")
    if df.empty:
        st.warning("目前沒有資料可以刪除。")
    else:
        selected_id = st.selectbox("選擇要刪除的商品ID", df["ID"].tolist())
        
        if st.button("刪除商品"):
            df = df[df["ID"] != selected_id]
            save_data(df)
            st.success("成功刪除商品！")
        
elif choice == "查看所有":
    st.subheader("所有保險商品資料")
    if df.empty:
        st.info("目前沒有任何商品資料。")
    else:
        st.dataframe(df)
