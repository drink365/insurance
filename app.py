import streamlit as st

st.title('💰 元大人壽龍億達保單試算平台')

# 使用者輸入區
gender = st.selectbox('性別', ['女', '男'])
age = st.number_input('年齡', min_value=0, max_value=120, value=40)
insured_amount = st.number_input('投保保額 (美元)', min_value=10000, value=1000000, step=10000)
pay_years = st.selectbox('繳費年期', [6])

st.subheader('試算結果：')

# 精準的實際資料（根據你提供）
real_data = {
    '解約金': {1: 25800, 5: 263200, 10: 377600, 20: 482100, 30: 604800, 40: 733200, 50: 848200, 60: 929100, 70: 986500},
    '身故保險金': {1: 1000000, 5: 1000000, 10: 1000000, 20: 1000000, 30: 1000000, 40: 1000000, 50: 1000000, 60: 1000000, 70: 1000000},
    '增值回饋分享金': {1: 499, 5: 4127, 10: 6004, 20: 8852, 30: 12825, 40: 17955, 50: 23988, 60: 30344, 70: 37207}
}

# 計算比例（以100萬美元為基準）
factor = insured_amount / 1000000

annual_premium = 60800 * factor
st.write(f'📌 **每年保費（折扣後）：** ${annual_premium:,.0f} 美元')

# 呈現各重要年度的解約金、身故保險金及增值回饋分享金
st.markdown('---')
st.subheader('📅 重要年度數據')

years = [1, 5, 10, 20, 30, 40, 50, 60, 70]

data_display = []
for year in years:
    data_display.append({
        '保單年度': year,
        '解約金': f"${real_data['解約金'][year]*factor:,.0f}",
        '身故保險金': f"${real_data['身故保險金'][year]*factor:,.0f}",
        '增值回饋分享金': f"${real_data['增值回饋分享金'][year]*factor:,.0f}"
    })

st.table(data_display)

st.markdown('---')
st.info('⚠️ 以上數據依據預定利率2.75%、宣告利率4.20%試算，實際數據將隨利率變動而有所不同，僅供參考。')
