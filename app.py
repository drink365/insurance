import streamlit as st

st.title('💰 元大人壽龍億達保單試算平台')

# 使用者輸入區
gender = st.selectbox('性別', ['男', '女'])
age = st.number_input('年齡', min_value=0, max_value=120, value=40)
insured_amount = st.number_input('投保保額 (美元)', min_value=10000, value=500000, step=10000)
pay_years = st.selectbox('繳費年期', [6, 12])

# 保費試算
if pay_years == 6:
    annual_premium = insured_amount * (30400 / 500000)  # 約6.08%
elif pay_years == 12:
    annual_premium = insured_amount * (16000 / 500000)  # 約3.20%

st.subheader('試算結果：')

st.write(f'📌 **每年保費：** ${annual_premium:,.0f} 美元')

# 增值回饋分享金試算（示範版）
bonus_rate = 0.00498 if pay_years == 6 else 0.004375
first_year_bonus = insured_amount * bonus_rate
st.write(f'📌 **第一年預估增值回饋分享金：** ${first_year_bonus:,.0f} 美元')

# 解約金試算（10年後示範）
surrender_value_rate_10yr = 0.3776 if pay_years == 6 else 0.318
surrender_value_10yr = insured_amount * surrender_value_rate_10yr
st.write(f'📌 **10年後解約金：** ${surrender_value_10yr:,.0f} 美元')

# 身故保險金試算（10年後示範）
death_benefit_rate_10yr = 1.1025 if pay_years == 6 else 1.06
death_benefit_10yr = insured_amount * death_benefit_rate_10yr
st.write(f'📌 **10年後身故或完全失能總給付：** ${death_benefit_10yr:,.0f} 美元')

st.markdown('---')
st.info('⚠️ 試算僅供參考，實際數值將依據當年度宣告利率及保單條款為準。')
