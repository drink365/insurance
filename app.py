import streamlit as st
import pandas as pd
import base64

st.title('📊 最佳保險方案試算平台')

# **Google Sheets CSV 下載連結**
gdrive_url = "https://docs.google.com/spreadsheets/d/你的文件ID/export?format=csv"

@st.cache_data
def load_google_sheets(url):
    return pd.read_csv(url)

try:
    # **讀取 Google Sheets 資料**
    df = load_google_sheets(gdrive_url)

    # **使用者輸入**
    sex = st.selectbox('性別', ['女', '男'])
    age = st.number_input('年齡', min_value=18, max_value=80, value=40, step=1)
    pay_years = st.selectbox('繳費年期', [6, 12])
    insured_amount = st.number_input('投保保額 (萬美元)', min_value=10, value=100, step=10)

    # **篩選符合條件的所有方案**
    filtered_df = df[
        (df["性別"] == sex) &
        (df["年齡"] == age) &
        (df["繳費年期"] == pay_years)
    ]

    if not filtered_df.empty:
        st.subheader('📌 最佳保險方案排序')
        
        important_years = [1, 5, 10, 20, 30]
        data_display = []

        for _, row in filtered_df.iterrows():
            product_name = row["商品名稱"]
            company_name = row["保險公司"]
            annual_premium = row["保費"] * (insured_amount / row["投保保額 (萬美元)"])

            entry = {
                '保險公司': company_name,
                '商品名稱': product_name,
                '年繳保費': f"${annual_premium:,.0f}"
            }
            
            for year in important_years:
                entry[f'{year}年後解約金'] = row[f"{year}年後解約金"] * (insured_amount / row["投保保額 (萬美元)"])
            
            data_display.append(entry)

        # **依據 30 年後解約金排序，最高排第一**
        sorted_data = sorted(data_display, key=lambda x: x['30年後解約金'], reverse=True)
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
            file_name=f'最佳保險方案試算.csv',
            mime='text/csv',
        )
    else:
        st.warning("⚠️ 無法找到符合條件的保險方案，請確認輸入條件")

except Exception as e:
    st.error("❌ 無法讀取 Google Sheets，請檢查權限是否正確！")
    st.text(str(e))
