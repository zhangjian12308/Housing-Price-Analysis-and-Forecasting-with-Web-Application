import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# 读取数据
file_path = "Data.csv"
data = pd.read_csv(file_path)

# 处理日期列
date_columns = data.columns[2:]
sorted_columns = sorted(date_columns, key=lambda x: pd.to_datetime(x, format='%m/%d/%Y'))
data_sorted = data[sorted_columns]

# 处理缺失值：按行前向+后向填充
data_filled = data_sorted.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)

# 计算平均价格
price_data = data_filled.mean()
price_data.index = pd.to_datetime(price_data.index, format='%m/%d/%Y')

# 确保时间序列没有缺失值
price_data = price_data.interpolate(method='time').ffill().bfill()

# 使用 Holt-Winters 进行时间序列预测
model = ExponentialSmoothing(price_data, trend="add", seasonal="add", seasonal_periods=3)
fitted_model = model.fit()

# 预测未来 5 个月价格
forecast_periods = 5
future_dates = pd.date_range(start=price_data.index[-1], periods=forecast_periods+1, freq='M')[1:]
future_predictions = fitted_model.forecast(steps=forecast_periods)

# 保存预测数据
forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Price": future_predictions})
forecast_df.to_csv("housing_forecast.csv", index=False)

# 绘制价格趋势及预测
plt.figure(figsize=(12, 6))
plt.plot(price_data.index, price_data, label="Historical Prices", color='blue')
plt.plot(future_dates, future_predictions, label="Predicted Prices", color='red', linestyle='dashed')
plt.xlabel("Date")
plt.ylabel("Average Housing Price")
plt.title("Housing Price Trend and Forecast")
plt.legend()
plt.grid(True)
plt.show()