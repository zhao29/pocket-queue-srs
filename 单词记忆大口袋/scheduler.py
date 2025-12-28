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

def daily_schedule():
    mu = predict_mu()
    print(f"【{datetime.now().date()}】预测明天μ = {mu:.2f}")
    a = 1
    b = -2*mu
    c = mu**2 - 12*mu
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        lambda_opt = 30
    else:
        lambda_opt = (-b - math.sqrt(discriminant)) / (2*a)
    new_cards_today = max(10, min(120, int(lambda_opt)))
    print(f"计划明天新词：{new_cards_today} 个")

if __name__ == "__main__":
    daily_schedule()
