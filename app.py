import streamlit as st
import pandas as pd
import os

# -------------------------
# 讀取 Streamlit Secrets 中的使用者憑證設定
# -------------------------
users = st.secrets["credentials"]

def login(account, password):
    """驗證帳號密碼，回傳使用者角色與顯示名稱"""
    if account in users and password == users[account]["password"]:
        return users[account]["role"], users[account].get("display_name", account)
    return None, None

# -------------------------
# 初始化 session_state
# -------------------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("role", None)
st.session_state.setdefault("display_name", None)
st.session_state.setdefault("login_success", False)

# -------------------------
# 登入介面（若未登入則顯示）
# -------------------------
if not st.session_state.logged_in:
    st.title("請登入")
    with st.form(key="login_form"):
        account = st.text_input("帳號")
        password = st.text_input("密碼", type="password")
        submit = st.form_submit_button("登入")
        if submit:
            role, display_name = login(account, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.display_name = display_name
                st.success(f"歡迎 {display_name}！")
                st.session_state.login_success = True
            else:
                st.error("帳號或密碼錯誤")
    
    # 登入成功後重新執行以更新頁面
    if st.session_state.get("login_success", False):
        st.session_state.login_success = False
        st.experimental_rerun()
    
    st.stop()  # 停止後續頁面顯示

# -------------------------
# 資料處理區
# -------------------------
DATA_FILE = 'insurance_products.csv'
COLUMNS = ["公司名", "商品名", "年期", "FYC", "獎勵金（文字）", "競賽計入"]

@st.cache_data
def load_data():
    """讀取或初始化資料檔案"""
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
    """儲存資料至 CSV 檔案"""
    df.to_csv(DATA_FILE, index=False)

df = load_data()

def get_key(row):
    """依據 公司名、商品名、年期 組合資料鍵"""
    return f"{row['公司名']} - {row['商品名']} - {row['年期']}"

def display_data(df):
    """將資料進行適度處理後顯示在介面上"""
    df_display = df.copy()
    if "key" in df_display.columns:
        df_display = df_display.drop(columns=["key"])
    df_display["FYC"] = df_display["FYC"].apply(lambda x: f"{x}%" if pd.notnull(x) else x)
    st.dataframe(df_display)

# -------------------------
# 主畫面：根據使用者權限呈現內容
# -------------------------
st.title("保險商品管理系統")
st.write(f"目前登入角色：{st.session_state.role}")

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
                # 檢查是否已存在相同的組合
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
            df_temp = df.copy()
            df_temp['key'] = df_temp.apply(get_key, axis=1)
            selected_key = st.selectbox("選擇要修改的項目", df_temp["key"].tolist(), key="modify_select")
            idx = df_temp.index[df_temp['key'] == selected_key][0]
            product = df_temp.loc[idx]

            new_公司名 = st.text_input("公司名", value=product["公司名"], key="modify_公司名")
            new_商品名 = st.text_input("商品名", value=product["商品名"], key="modify_商品名")
            new_年期 = st.number_input("年期", min_value=1, step=1, value=int(product["年期"]), key="modify_年期")
            new_FYC = st.number_input("FYC (%)", min_value=0.0, step=0.1, value=float(product["FYC"]), key="modify_FYC")
            new_獎勵金 = st.text_area("獎勵金（文字）", value=product["獎勵金（文字）"], key="modify_獎勵金")
            default_index = 0 if product["競賽計入"] == "計入" else 1
            new_競賽計入 = st.selectbox("競賽計入", ["計入", "不計入"], index=default_index, key="modify_競賽計入")
            
            if st.button("儲存修改", key="modify_button"):
                # 找到原始資料的 index
                orig_idx = df.index[(df["公司名"] == product["公司名"]) &
                                    (df["商品名"] == product["商品名"]) &
                                    (df["年期"] == product["年期"])][0]
                df.at[orig_idx, "公司名"] = new_公司名
                df.at[orig_idx, "商品名"] = new_商品名
                df.at[orig_idx, "年期"] = new_年期
                df.at[orig_idx, "FYC"] = new_FYC
                df.at[orig_idx, "獎勵金（文字）"] = new_獎勵金
                df.at[orig_idx, "競賽計入"] = new_競賽計入
                save_data(df)
                st.success("成功修改商品資料！")

    # --- 刪除資料 ---
    with tabs[2]:
        st.subheader("刪除保險商品資料")
        if df.empty:
            st.warning("目前沒有資料可以刪除。")
        else:
            df_temp = df.copy()
            df_temp['key'] = df_temp.apply(get_key, axis=1)
            selected_key_del = st.selectbox("選擇要刪除的項目", df_temp["key"].tolist(), key="delete_select")
            if st.button("刪除資料", key="delete_button"):
                df = df[df_temp['key'] != selected_key_del]
                save_data(df)
                st.success("成功刪除資料！")

    # --- 檢視資料 ---
    with tabs[3]:
        st.subheader("所有保險商品資料")
        if df.empty:
            st.info("目前沒有任何商品資料。")
        else:
            display_data(df)

else:
    # 使用者角色：僅能檢視資料
    st.subheader("所有保險商品資料")
    if df.empty:
        st.info("目前沒有任何商品資料。")
    else:
        display_data(df)
