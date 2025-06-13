from flask import Flask, Response
import random
import time
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# 定义指标
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage in percent')
memory_usage = Gauge('memory_usage_mb', 'Memory usage in MB')
request_count = Counter('http_requests_total', 'Total HTTP requests')
error_count = Counter('http_errors_total', 'Total HTTP errors')

@app.route('/metrics')
def metrics():
    # 更新指标值
    cpu_usage.set(random.uniform(0, 100))
    memory_usage.set(random.uniform(100, 1000))
    request_count.inc()
    
    # 随机生成一些错误
    if random.random() < 0.1:  # 10%的概率生成错误
        error_count.inc()
    
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/')
def index():
    return 'Metrics server is running. Visit /metrics to see the metrics.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 