import streamlit as st
import pandas as pd
import os

# -------------------------
# 從 Streamlit Secrets 讀取帳號與權限設定
# -------------------------
# secrets 中應該設定 credentials 為一個字典，格式如下：
# [credentials]
# admin = { password = "admin123", role = "管理者" }
# user = { password = "user123", role = "使用者" }
#
# 請務必在 Streamlit Cloud 的 Secrets 管理介面中設定，或在本地建立 .streamlit/secrets.toml
users = st.secrets["credentials"]

def login(username, password):
    if username in users and password == users[username]["password"]:
        return users[username]["role"]
    else:
        return None

# 初始化 session_state 登入狀態
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# -------------------------
# 登入介面（未登入時停留在此頁）
# -------------------------
if not st.session_state.logged_in:
    st.title("請登入")
    username = st.text_input("使用者名稱")
    password = st.text_input("密碼", type="password")
    if st.button("登入"):
        role = login(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success(f"登入成功！歡迎 {username} ({role})")
        else:
            st.error("使用者名稱或密碼錯誤")
    st.stop()  # 未登入前不執行後續程式

# -------------------------
# 登入後主要介面
# -------------------------
st.title("保險商品管理系統")
st.write(f"目前登入角色：{st.session_state.role}")

# -------------------------
# 資料處理函式
# -------------------------
DATA_FILE = 'insurance_products.csv'
COLUMNS = ["公司名", "商品名", "年期", "FYC", "獎勵金（文字）", "競賽計入"]

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        missing_cols = [col for col in COLUMNS if col not in df.columns]
        if missing_cols:
            st.warning(f"資料檔案缺少欄位: {missing_cols}，將重新初始化資料。")
            df = pd.DataFrame(columns=COLUMNS)
            df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# -------------------------
# 根據權限自動呈現頁面內容
# -------------------------
# 管理者功能：新增、修改、刪除、檢視（利用 tabs 分區）
# 使用者功能：僅能檢視資料（可點表頭排序）
if st.session_state.role == "管理者":
    tabs = st.tabs(["新增", "修改", "刪除", "查看"])
    
    # --- 新增資料 ---
    with tabs[0]:
        st.subheader("新增保險商品資料")
        公司名 = st.text_input("公司名", key="add_公司名")
        商品名 = st.text_input("商品名", key="add_商品名")
        年期 = st.number_input("年期", min_value=1, step=1, key="add_年期")
        FYC_value = st.number_input("FYC (%)", min_value=0.0, step=0.1, key="add_FYC")
        獎勵金 = st.text_area("獎勵金（文字）", key="add_獎勵金")
        競賽計入 = st.selectbox("競賽計入", ["計入", "不計入"], key="add_競賽計入")
        if st.button("新增商品", key="add_button"):
            if 公司名 and 商品名:
                # 檢查是否已存在相同公司名、商品名及年期的組合
                if ((df["公司名"] == 公司名) & (df["商品名"] == 商品名) & (df["年期"] == 年期)).any():
                    st.error("該公司名、商品名與年期的組合已存在，請使用不同的資料。")
                else:
                    new_data = {
                        "公司名": 公司名,
                        "商品名": 商品名,
                        "年期": 年期,
                        "FYC": FYC_value,
                        "獎勵金（文字）": 獎勵金,
                        "競賽計入": 競賽計入
                    }
                    df = pd.concat([df, pd.DataFrame(new_data, index=[0])], ignore_index=True)
                    save_data(df)
                    st.success("成功新增商品資料！")
            else:
                st.error("請填入必填欄位：公司名與商品名。")
    
    # --- 修改資料 ---
    with tabs[1]:
        st.subheader("修改保險商品資料")
        if df.empty:
            st.warning("目前沒有資料可以修改。")
        else:
            # 建立唯一識別 key，格式： 公司名 - 商品名 - 年期
            df['key'] = df["公司名"] + " - " + df["商品名"] + " - " + df["年期"].astype(str)
            selected_key = st.selectbox("選擇要修改的項目", df["key"].tolist(), key="modify_select")
            idx = df.index[df['key'] == selected_key][0]
            product = df.loc[idx]
            
            new_公司名 = st.text_input("公司名", value=product["公司名"], key="modify_公司名")
            new_商品名 = st.text_input("商品名", value=product["商品名"], key="modify_商品名")
            new_年期 = st.number_input("年期", min_value=1, step=1, value=int(product["年期"]), key="modify_年期")
            new_FYC = st.number_input("FYC (%)", min_value=0.0, step=0.1, value=float(product["FYC"]), key="modify_FYC")
            new_獎勵金 = st.text_area("獎勵金（文字）", value=product["獎勵金（文字）"], key="modify_獎勵金")
            default_index = 0 if product["競賽計入"] == "計入" else 1
            new_競賽計入 = st.selectbox("競賽計入", ["計入", "不計入"], index=default_index, key="modify_競賽計入")
            if st.button("儲存修改", key="modify_button"):
                df.at[idx, "公司名"] = new_公司名
                df.at[idx, "商品名"] = new_商品名
                df.at[idx, "年期"] = new_年期
                df.at[idx, "FYC"] = new_FYC
                df.at[idx, "獎勵金（文字）"] = new_獎勵金
                df.at[idx, "競賽計入"] = new_競賽計入
                df = df.drop(columns=["key"])
                save_data(df)
                st.success("成功修改商品資料！")
    
    # --- 刪除資料 ---
    with tabs[2]:
        st.subheader("刪除保險商品資料")
        if df.empty:
            st.warning("目前沒有資料可以刪除。")
        else:
            df['key'] = df["公司名"] + " - " + df["商品名"] + " - " + df["年期"].astype(str)
            selected_key_del = st.selectbox("選擇要刪除的項目", df["key"].tolist(), key="delete_select")
            if st.button("刪除資料", key="delete_button"):
                df = df[df['key'] != selected_key_del]
                df = df.drop(columns=["key"])
                save_data(df)
                st.success("成功刪除資料！")
    
    # --- 檢視資料 ---
    with tabs[3]:
        st.subheader("所有保險商品資料")
        if df.empty:
            st.info("目前沒有任何商品資料。")
        else:
            df_display = df.copy()
            df_display["FYC"] = df_display["FYC"].apply(lambda x: f"{x}%" if pd.notnull(x) else x)
            st.dataframe(df_display)  # 內建互動排序

else:
    # 使用者角色：僅能檢視資料
    st.subheader("所有保險商品資料")
    if df.empty:
        st.info("目前沒有任何商品資料。")
    else:
        df_display = df.copy()
        df_display["FYC"] = df_display["FYC"].apply(lambda x: f"{x}%" if pd.notnull(x) else x)
        st.dataframe(df_display)
