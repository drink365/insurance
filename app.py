import streamlit as st
import pandas as pd
import os

# 定義 CSV 檔案儲存路徑與正確欄位
DATA_FILE = 'insurance_products.csv'
COLUMNS = ["公司名", "商品名", "年期", "來佣率", "獎勵金（文字）", "競賽計入"]

# 載入資料，並檢查欄位是否完整
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # 檢查 CSV 中是否有缺少預期欄位
        missing_cols = [col for col in COLUMNS if col not in df.columns]
        if missing_cols:
            st.warning(f"資料檔案缺少欄位: {missing_cols}，將重新初始化資料。")
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)
    return df

# 儲存資料到 CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Streamlit 介面標題與說明
st.title("保險商品管理系統")
st.write("請利用側邊選單來選擇操作功能：新增、修改、刪除或檢視所有商品資料。")

# 載入現有資料
df = load_data()

# 側邊選單
menu = ["新增", "修改", "刪除", "查看所有"]
choice = st.sidebar.selectbox("選擇操作", menu)

if choice == "新增":
    st.subheader("新增保險商品資料")
    公司名 = st.text_input("公司名")
    商品名 = st.text_input("商品名")
    年期 = st.number_input("年期", min_value=1, step=1)
    來佣率 = st.number_input("來佣率", min_value=0.0, step=0.1)
    獎勵金 = st.text_area("獎勵金（文字）")
    競賽計入 = st.selectbox("競賽計入", ["計入", "不計入"])
    
    if st.button("新增商品"):
        if 公司名 and 商品名:
            # 檢查是否已存在相同的公司名與商品名組合
            if ((df["公司名"] == 公司名) & (df["商品名"] == 商品名)).any():
                st.error("該公司名與商品名的組合已存在，請使用不同的資料。")
            else:
                new_data = {
                    "公司名": 公司名,
                    "商品名": 商品名,
                    "年期": 年期,
                    "來佣率": 來佣率,
                    "獎勵金（文字）": 獎勵金,
                    "競賽計入": 競賽計入
                }
                # 用 pd.concat 替代 df.append
                df = pd.concat([df, pd.DataFrame(new_data, index=[0])], ignore_index=True)
                save_data(df)
                st.success("成功新增商品資料！")
        else:
            st.error("請填入必填欄位：公司名與商品名。")
                
elif choice == "修改":
    st.subheader("修改保險商品資料")
    if df.empty:
        st.warning("目前沒有資料可以修改。")
    else:
        # 建立一個組合欄位（公司名 - 商品名）作為識別 key
        df['key'] = df["公司名"] + " - " + df["商品名"]
        selected_key = st.selectbox("選擇要修改的項目", df["key"].tolist())
        idx = df.index[df['key'] == selected_key][0]
        product = df.loc[idx]
        
        公司名 = st.text_input("公司名", value=product["公司名"])
        商品名 = st.text_input("商品名", value=product["商品名"])
        年期 = st.number_input("年期", min_value=1, step=1, value=int(product["年期"]))
        來佣率 = st.number_input("來佣率", min_value=0.0, step=0.1, value=float(product["來佣率"]))
        獎勵金 = st.text_area("獎勵金（文字）", value=product["獎勵金（文字）"])
        default_index = 0 if product["競賽計入"] == "計入" else 1
        競賽計入 = st.selectbox("競賽計入", ["計入", "不計入"], index=default_index)
        
        if st.button("儲存修改"):
            df.at[idx, "公司名"] = 公司名
            df.at[idx, "商品名"] = 商品名
            df.at[idx, "年期"] = 年期
            df.at[idx, "來佣率"] = 來佣率
            df.at[idx, "獎勵金（文字）"] = 獎勵金
            df.at[idx, "競賽計入"] = 競賽計入
            df = df.drop(columns=["key"])
            save_data(df)
            st.success("成功修改商品資料！")
        
elif choice == "刪除":
    st.subheader("刪除保險商品資料")
    if df.empty:
        st.warning("目前沒有資料可以刪除。")
    else:
        df['key'] = df["公司名"] + " - " + df["商品名"]
        selected_key = st.selectbox("選擇要刪除的項目", df["key"].tolist())
        if st.button("刪除資料"):
            df = df[df['key'] != selected_key]
            df = df.drop(columns=["key"])
            save_data(df)
            st.success("成功刪除資料！")
        
elif choice == "查看所有":
    st.subheader("所有保險商品資料")
    if df.empty:
        st.info("目前沒有任何商品資料。")
    else:
        st.dataframe(df)
