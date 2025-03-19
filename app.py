import streamlit as st
import pandas as pd
import base64

st.title('📊 保險商品試算平台')

# **Google Sheets CSV 下載連結**
gdrive_url = "https://docs.google.com/spreadsheets/d/你的文件ID/export?format=csv"

@st.cache_data
def load_google_sheets(url):
    return pd.read_csv(url)

try:
    # **讀取 Google Sheets 資料**
    df = load_google_sheets(gdrive_url)

    # **篩選可用的保險公司和商品**
    companies = df["保險公司"].unique()
    selected_company = st.selectbox("選擇保險公司", companies)

    products = df[df["保險公司"] == selected_company]["商品名稱"].unique()
    selected_product = st.selectbox("選擇保險商品", products)

    # **使用者輸入**
    sex = st.selectbox('性別', ['女', '男'])
    age = st.number_input('年齡', min_value=18, max_value=80, value=40, step=1)
    pay_years = st.selectbox('繳費年期', [6, 12])
    insured_amount = st.number_input('投保保額 (萬美元)', min_value=10, value=100, step=10)

    # **篩選符合條件的資料**
    filtered_df = df[
        (df["保險公司"] == selected_company) &
        (df["商品名稱"] == selected_product) &
        (df["性別"] == sex) &
        (df["年齡"] == age) &
        (df["繳費年期"] == pay_years)
    ]

    if not filtered_df.empty:
        annual_premium = filtered_df.iloc[0]["保費"]
        st.subheader('📌 試算結果')
        st.write(f'每年保費：**${annual_premium:,.0f}** 美元')

        # **關鍵年份數據並排序（解約金從高到低）**
        important_years = [1, 5, 10, 20, 30]
        data_display = []

        for year in important_years:
            cash_value = filtered_df.iloc[0][f"{year}年後解約金"]
            death_benefit = insured_amount * 10000  # 假設身故保險金為固定保額
            data_display.append({
                '保單年度': year,
                '解約金': cash_value,
                '身故保險金': death_benefit
            })

        # 排序（解約金從高到低）
        sorted_data = sorted(data_display, key=lambda x: x['解約金'], reverse=True)
        sorted_df = pd.DataFrame(sorted_data)

        st.table(sorted_df)
        st.info('⚠️ 試算結果僅供參考，實際數據依保單條款與宣告利率而有所變動')

        # **提供下載 Excel 功能**
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(sorted_df)
        st.download_button(
            label="📥 下載 Excel 試算結果",
            data=csv,
            file_name=f'{selected_company}_{selected_product}_試算結果.csv',
            mime='text/csv',
        )
    else:
        st.warning("⚠️ 無法找到符合條件的保費與解約金資料，請確認輸入條件")

except Exception as e:
    st.error("❌ 無法讀取 Google Sheets，請檢查權限是否正確！")
    st.text(str(e))
