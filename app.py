import streamlit as st
import pandas as pd

st.title('💰 保單試算平台 - 依據使用者輸入計算')

# **使用者輸入**
sex = st.selectbox('性別', ['女', '男'])
age = st.number_input('年齡', min_value=18, max_value=80, value=40, step=1)
pay_years = st.selectbox('繳費年期', [6, 12])
insured_amount = st.number_input('投保保額 (美元)', min_value=10000, value=1000000, step=10000)

# **Google Sheets CSV 下載連結**
gdrive_url = "https://docs.google.com/spreadsheets/d/1ITlpwQNV29tWOqcNoTHRq9R3iENoPisp/export?format=csv"

@st.cache_data
def load_google_sheets(url):
    return pd.read_csv(url)

try:
    # **讀取 Google Sheets 資料**
    df = load_google_sheets(gdrive_url)

    # **篩選符合條件的資料**
    sex_code = 'F' if sex == '女' else 'M'
    filtered_df = df[(df['Sex'] == sex_code) & (df['Age'] == age) & (df['Yearly'] == pay_years)]

    if not filtered_df.empty:
        base_premium = filtered_df.iloc[0]['Annual_Premium']
        annual_premium = base_premium * (insured_amount / 1000000)

        st.subheader('📌 試算結果')
        st.write(f'每年保費：**${annual_premium:,.0f}** 美元')

        # **關鍵年份數據**
        important_years = [1, 5, 10, 20, 30, 40]
        data_display = []

        for year in important_years:
            if str(year) in filtered_df.columns:
                cash_value = filtered_df.iloc[0][str(year)] * (insured_amount / 1000000)
                death_benefit = insured_amount  # 假設身故保險金為固定保額
                data_display.append({
                    '保單年度': year,
                    '解約金': f"${cash_value:,.0f}",
                    '身故保險金': f"${death_benefit:,.0f}"
                })

        st.table(data_display)

        st.info('⚠️ 試算結果僅供參考，實際數據依保單條款與宣告利率而有所變動')

    else:
        st.warning("⚠️ 無法找到符合條件的保費與解約金資料，請確認輸入條件")

except Exception as e:
    st.error("❌ 無法讀取 Google Sheets，請檢查權限是否正確！")
    st.text(str(e))
