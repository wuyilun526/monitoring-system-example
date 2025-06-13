# Prometheus Monitoring Stack Example

This project uses Docker Compose to set up a complete monitoring system, including:
- **Flask**: Simulates continuous generation of time series metrics data
- **Prometheus**: Collects and stores metrics data
- **Grafana**: Visualizes monitoring data
- **Alertmanager**: Manages alerts

## Quick Start

### 1. Clone the Project

```bash
git clone git@github.com:wuyilun526/monitoring-system-example.git
cd monitoring-system-example
```

### 2. Start the Services

```bash
docker-compose up -d
```

### 3. Access the Services

- Flask metrics endpoint: [http://localhost:5000/metrics](http://localhost:5000/metrics)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000)  
  Default username/password: `admin` / `admin`
- Alertmanager: [http://localhost:9093](http://localhost:9093)

## Project Structure

```
.
├── app/                    # Flask application
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── prometheus/             # Prometheus configuration
│   ├── prometheus.yml
│   └── alert_rules.yml
├── grafana/                # Grafana configuration
│   └── provisioning/
│       └── datasources/
│           └── datasource.yml
├── alertmanager/           # Alertmanager configuration
│   └── alertmanager.yml
├── docker-compose.yml
└── README.md
```

## Metrics

- `cpu_usage_percent`: CPU usage percentage
- `memory_usage_mb`: Memory usage in MB
- `http_requests_total`: Total HTTP requests
- `http_errors_total`: Total HTTP errors

## Alert Rules

- CPU usage above 80%
- Memory usage above 800MB
- Error rate above 10%

## Local Development

To run the Flask app locally:

```bash
cd app
pip install -r requirements.txt
python app.py
```

## License

MIT
