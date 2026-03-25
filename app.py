from flask import Flask
from routes.webhook import webhook_bp

app = Flask(__name__)
app.register_blueprint(webhook_bp, url_prefix="/webhook")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
