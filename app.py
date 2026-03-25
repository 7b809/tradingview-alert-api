from flask import Flask
from routes.webhook import webhook_bp

app = Flask(__name__)
app.register_blueprint(webhook_bp, url_prefix="/webhook")
from routes.alerts import alerts_bp   # ✅ ADD

app.register_blueprint(alerts_bp, url_prefix="/alerts")  # ✅ ADD

if __name__ == "__main__":
    app.run(port=5000, debug=True)
