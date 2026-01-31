import sqlite3
import pandas as pd
import statsmodels.api as sm
import math
from datetime import datetime

DB = 'srs.db'

def predict_mu():
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM daily_log WHERE sleep IS NOT NULL ORDER BY date DESC LIMIT 30", conn)
    conn.close()
    if len(df) < 10:
        return 4.0
    X = df[['sleep', 'afternoon_hours', 'evening_hours', 'avg_difficulty', 'load_last_hour']].fillna(0)
    X = sm.add_constant(X)
    y = df['reviews_done'].fillna(50) / (df['avg_difficulty'].fillna(0.5).mean() + 0.5)
    try:
        model = sm.OLS(y, X).fit()
        last = df.iloc[0]
        pred = model.predict([[1, last['sleep'] or 7, last['afternoon_hours'] or 0, last['evening_hours'] or 0, last['avg_difficulty'] or 0.5, last['load_last_hour'] or 50]])[0]
    except:
        pred = 4.0
    return max(1.5, min(pred, 8.0))

def predict_lq(lambda_, mu):
    """M/G/1队列长度预测（兼容原M/M/1行为）"""
    if mu <= lambda_:
        return float('inf')  # 系统不稳定
    rho = lambda_ / mu
    var_s = 1 / (mu ** 2)  # 假设指数分布服务时间方差（与M/M/1一致）
    # 如需更一般M/G/1，可后续从数据估计var_s
    lq = (lambda_ ** 2 * var_s + rho ** 2) / (2 * (1 - rho))
    return lq

def daily_schedule():
    mu = predict_mu()
    print(f"【{datetime.now().date()}】预测明天μ = {mu:.2f}")
    
    # 用简单搜索找最大新词量，使预测Lq ≤15
    max_new = 180
    min_new = 10
    best_lambda = min_new
    for lambda_test in range(max_new, min_new - 1, -1):  # 从高到低试
        if predict_lq(lambda_test, mu) <= 15:
            best_lambda = lambda_test
            break
    
    new_cards_today = best_lambda
    print(f"计划明天新词：{new_cards_today} 个（基于M/G/1模型，Lq阈值15）")

if __name__ == "__main__":
    daily_schedule()
