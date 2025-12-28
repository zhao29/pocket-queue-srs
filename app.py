from flask import Flask
from scheduler import daily_schedule

app = Flask(__name__)

@app.route('/')
def index():
    daily_schedule()
    return '''
    <h1>队列背单词系统（已启动！）</h1>
    <p>控制台会显示明天的学习计划</p>
    <p>系统运行正常，核心算法已执行。</p>
    <button onclick="location.reload()">重新计算明天计划</button>
    '''

if __name__ == '__main__':
    print("服务器启动了！浏览器打开 http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
