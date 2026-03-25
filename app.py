from flask import Flask, jsonify
from config import Config
from routes.webhook import webhook_bp
from routes.alerts import alerts_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(webhook_bp, url_prefix="/webhook")
    app.register_blueprint(alerts_bp, url_prefix="/alerts")

    # ✅ Home Route
    @app.route("/")
    def home():
        return jsonify({
            "message": "TradingView Webhook API is running 🚀",
            "routes": {
                "health": "/health",
                "webhook": "/webhook/",
                "alerts": "/alerts/",
                "alerts_page": "/alerts/<page>"
            }
        })

    # ✅ Health Check
    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.FLASK_PORT, debug=True)