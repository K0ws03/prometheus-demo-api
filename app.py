from flask import Flask
import time
import random

app = Flask(__name__)

# We'll track this counter
request_count = 0

@app.route("/")
def hello():
  return "Hello from Prometheus Demo API"

@app.route("/counter")
def counter():
  global request_count
  request_count+=1
  return f"Counter: {request_count}"

@app.route("/slow")
def slow():
  # Random delay between 0.1 and 2 seconds
  time.sleep(random.uniform(0.1,0.2))
  return "This was slow"

@app.route("/error")
def error():
  # Fail 30% of the time
  if random.random() < 0.3:
    return "Error occured", 500
  return "Success"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, debug=True)