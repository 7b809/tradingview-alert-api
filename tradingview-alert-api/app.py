from flask import Flask
from config import Config
from routes import webhook


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(webhook)

    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.FLASK_PORT)
