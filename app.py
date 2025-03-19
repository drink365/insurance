import streamlit as st
import pandas as pd

# 讀取現金價值與保費資料
xlsm_file_path = '/mnt/data/元大人壽-KO(龍億達美元)試算表_經代版【114.03.01】.xlsm'
cv_df = pd.read_excel(xlsm_file_path, sheet_name="CV", engine="openpyxl")
gp_df = pd.read_excel(xlsm_file_path, sheet_name="GP", engine="openpyxl")

st.title('💰 保單試算平台 - 龍億達美元利率變動型終身壽險')

# 讓使用者選擇參數
sex = st.selectbox('性別', ['女', '男'])
age = st.number_input('年齡', min_value=0, max_value=100, value=40, step=1)
pay_years = st.selectbox('繳費年期', [6])
insured_amount = st.number_input('投保保額 (美元)', min_value=10000, value=1000000, step=10000)

# 將性別轉換為Excel格式 (F, M)
sex_code = 'F' if sex == '女' else 'M'

# **查找保費**
gp_row = gp_df[(gp_df['Sex'] == sex_code) & (gp_df['Yearly'] == pay_years) & (gp_df['Age'] == age)]
if not gp_row.empty:
    base_premium = gp_row.iloc[0, 4]  # 取該年齡對應的保費
    annual_premium = base_premium * (insured_amount / 1000000)
else:
    annual_premium = '無對應資料'

st.subheader('📌 試算結果')
st.write(f'每年保費：**${annual_premium:,.0f}** 美元' if isinstance(annual_premium, (int, float)) else '無法計算保費')

# **查找現金價值**
cv_row = cv_df[(cv_df['Sex'] == sex_code) & (cv_df['Yearly'] == pay_years) & (cv_df['Age'] == age)]

data_display = []
important_years = [1, 5, 10, 20, 30, 40, 50, 60, 70]
if not cv_row.empty:
    for year in important_years:
        if str(year) in cv_row.columns:
            cash_value = cv_row[str(year)].values[0] * (insured_amount / 1000000)
            data_display.append({'保單年度': year, '解約金': f"${cash_value:,.0f}"})
else:
    st.write("未找到對應的現金價值數據")

# 顯示解約金表格
if data_display:
    st.table(data_display)

st.info('⚠️ 試算結果僅供參考，實際數據依保單條款與宣告利率而有所變動')
