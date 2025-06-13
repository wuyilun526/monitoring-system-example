from flask import Flask, Response
import random
import time
import multiprocessing
import os
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import threading

# 定义指标，使用进程ID来区分不同进程的指标
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage in percent', ['process_id'])
memory_usage = Gauge('memory_usage_mb', 'Memory usage in MB', ['process_id'])
request_count = Counter('http_requests_total', 'Total HTTP requests', ['process_id'])
error_count = Counter('http_errors_total', 'Total HTTP errors', ['process_id'])

def generate_metrics(pid):
    """持续生成CPU和内存指标"""
    while True:
        try:
            # 更新指标值
            cpu_usage.labels(process_id=str(pid)).set(random.uniform(50, 100))
            memory_usage.labels(process_id=str(pid)).set(random.uniform(500, 1000))
            time.sleep(1)
        except Exception as e:
            print(f"Error in metrics generation: {e}")

def create_app(port, pid):
    """为每个端口创建独立的Flask应用"""
    app = Flask(__name__)
    
    @app.route('/metrics')
    def metrics():
        # 根据端口确定错误概率
        error_probability = 0.5 if port == 8000 else 0.1  # 第一个端口50%错误率，其他端口10%错误率
        
        # 更新请求计数
        request_count.labels(process_id=str(pid)).inc()
        
        # 根据概率生成错误
        if random.random() < error_probability:
            error_count.labels(process_id=str(pid)).inc()
        
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    @app.route('/')
    def index():
        return f'Metrics server is running (PID: {pid}, Port: {port}). Visit /metrics to see the metrics.'
    
    return app

def run_app(port):
    """运行Flask应用并启动指标生成器"""
    pid = os.getpid()  # 在子进程中获取PID
    app = create_app(port, pid)
    
    # 使用线程来生成指标
    metrics_thread = threading.Thread(target=generate_metrics, args=(pid,))
    metrics_thread.daemon = True
    metrics_thread.start()
    
    # 启动Flask应用
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # 启动3个进程，每个进程使用不同的端口
    ports = [8000, 8001, 8002]  # 使用8000系列端口
    processes = []
    
    for port in ports:
        p = multiprocessing.Process(target=run_app, args=(port,))
        p.daemon = True
        p.start()
        processes.append(p)
    
    # 等待所有进程
    for p in processes:
        p.join() 