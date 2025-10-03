from flask import Flask, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
import random

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "app_requests_total", "Total number of requests", ["endpoint", "method", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_requests_duration_seconds", "Request latency in seconds", ["endpoint"]
)

ACTIVE_REQUESTS = Gauge(
    "app_active_requests", "Number of requests currently being processed"
)

COUNTER_VALUE = Gauge("app_counter_value", "Current value of the counter")

# We'll track this counter
request_count = 0


@app.route("/")
def hello():
    ACTIVE_REQUESTS.inc()
    start = time.time()
    response = "Hello from Prometheus Demo API"
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)
    REQUEST_COUNT.labels(endpoint="/", method="GET", status=200).inc()
    ACTIVE_REQUESTS.dec()
    return response


@app.route("/counter")
def counter():
    ACTIVE_REQUESTS.inc()
    start = time.time()
    global request_count
    request_count += 1
    COUNTER_VALUE.set(request_count)
    response = f"Counter: {request_count}"
    REQUEST_LATENCY.labels(endpoint="/counter").observe(time.time() - start)
    REQUEST_COUNT.labels(endpoint="/counter", method="GET", status=200).inc()
    ACTIVE_REQUESTS.dec()
    return response


@app.route("/slow")
def slow():
    ACTIVE_REQUESTS.inc()
    start = time.time()
    # Random delay between 0.1 and 2 seconds
    time.sleep(random.uniform(0.1, 2))
    REQUEST_LATENCY.labels(endpoint="/slow").observe(time.time() - start)
    REQUEST_COUNT.labels(endpoint="/slow", method="GET", status=200).inc()
    ACTIVE_REQUESTS.dec()
    return "This was slow"


@app.route("/error")
def error():
    ACTIVE_REQUESTS.inc()
    start = time.time()
    # Fail 30% of the time
    if random.random() < 0.3:
        REQUEST_LATENCY.labels(endpoint="/error").observe(time.time() - start)
        REQUEST_COUNT.labels(endpoint="/error", method="GET", status=500).inc()
        ACTIVE_REQUESTS.dec()
        return "Error occured", 500
    REQUEST_LATENCY.labels(endpoint="/error").observe(time.time() - start)
    REQUEST_COUNT.labels(endpoint="/error", method="GET", status=200).inc()
    ACTIVE_REQUESTS.dec()
    return "Success"


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(), mimetype="text/plain; version=0.0.4; charset=utf-8"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
