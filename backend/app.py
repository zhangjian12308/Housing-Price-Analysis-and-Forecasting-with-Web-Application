from flask import Flask, jsonify, request
import sqlite3
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许前端访问后端 API

DATABASE = "housing_data.db"

# 获取数据库连接
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 获取所有房价数据
@app.route('/api/housing-data', methods=['GET'])
def get_housing_data():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM housing_prices", conn)
    conn.close()
    return jsonify(df.to_dict(orient="records"))

# 预测未来房价
@app.route('/api/forecast', methods=['GET'])
def forecast_price():
    months = int(request.args.get('months', 5))  # 默认预测 5 个月

    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM housing_prices", conn)
    conn.close()
    
    # 计算平均价格时间序列
    price_series = df.groupby("date")["price"].mean()
    price_series.index = pd.to_datetime(price_series.index)

    # 使用 Holt-Winters 进行时间序列预测
    model = ExponentialSmoothing(price_series, trend="add", seasonal="add", seasonal_periods=3)
    fitted_model = model.fit()
    future_dates = pd.date_range(start=price_series.index[-1], periods=months+1, freq='M')[1:]
    predictions = fitted_model.forecast(steps=months)

    # 返回预测结果
    result = {str(date.date()): price for date, price in zip(future_dates, predictions)}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
