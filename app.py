"""
Module for calling the main flask application.
The application will be only supported with Flask and Gunicorn.
"""
from flask import Flask, json
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from router.attendance import route as create_record
from router.cache import cache
from utils.json_encoder import DataclassJSONEncoder
from client.redis.redis_conn import get_caching_data
from flask_cors import CORS
import os

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# ALB DNS URL
ALB_DNS = os.getenv("ALB_DNS", "http://OT-MS-Load-Balancer-1191154576.ap-south-1.elb.amazonaws.com")

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # Include all endpoints
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    # Explicitly tell Swagger where to fetch the JSON
    "swagger_ui_config": {
        "url": f"{ALB_DNS}/apispec_1.json"
    }
}

swagger = Swagger(app, config=swagger_config)

# Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info("attendance_api", "Attendance API opentelemetry metrics", version="0.1.0")

# Initialize cache
cache.init_app(app, get_caching_data())

# JSON settings
app.config['JSON_SORT_KEYS'] = False
json.provider.DefaultJSONProvider.sort_keys = False
app.json_encoder = DataclassJSONEncoder

# Register blueprint
app.register_blueprint(create_record, url_prefix="/api/v1")

if __name__ == "__main__":
    # For local testing
    app.run(host="0.0.0.0", port=5001, debug=True)
