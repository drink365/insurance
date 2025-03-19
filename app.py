import pandas as pd
import numpy as np

# 定義變數範圍
companies = ["A公司", "B公司", "C公司"]
products = ["終身壽險", "定期壽險", "投資型壽險"]
sex_list = ["男", "女"]
ages = np.arange(18, 70, 2)  # 18~70歲，間隔2歲
pay_years_list = [6, 12, 20]  # 繳費年期
insured_amounts = [50, 100, 200, 500]  # 投保保額 (萬美元)

# 創建數據列表
data = []

for company in companies:
    for product in products:
        for sex in sex_list:
            for age in ages:
                for pay_years in pay_years_list:
                    for insured_amount in insured_amounts:
                        base_premium = 1000 + (age * 5) + (pay_years * 20)  # 保費計算公式
                        annual_premium = base_premium * (insured_amount / 100)

                        # 解約金（簡單模擬增長）
                        surrender_values = {
                            "1年後解約金": annual_premium * 0.2,
                            "5年後解約金": annual_premium * 1.5,
                            "10年後解約金": annual_premium * 3,
                            "20年後解約金": annual_premium * 5,
                            "30年後解約金": annual_premium * 7
                        }

                        data.append([
                            company, product, sex, age, pay_years, insured_amount,
                            annual_premium, surrender_values["1年後解約金"], surrender_values["5年後解約金"],
                            surrender_values["10年後解約金"], surrender_values["20年後解約金"], surrender_values["30年後解約金"]
                        ])

# 轉為 DataFrame
columns = ["保險公司", "商品名稱", "性別", "年齡", "繳費年期", "投保保額 (萬美元)", "保費",
           "1年後解約金", "5年後解約金", "10年後解約金", "20年後解約金", "30年後解約金"]
df = pd.DataFrame(data, columns=columns)

# 匯出 CSV
csv_filename = "/mnt/data/insurance_products_generated.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

# 顯示下載連結
import ace_tools as tools
tools.display_dataframe_to_user(name="保險試算數據", dataframe=df)
print(f"✅ 已生成試算數據，請下載 CSV 檔案並上傳到 Google Sheets：{csv_filename}")
