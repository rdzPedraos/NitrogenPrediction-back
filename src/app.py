from flask import Flask
from config import Config
from extensions import socketio
from routes import main_blueprint

app = Flask(__name__)
app.config.from_object(Config)

socketio.init_app(app)

# Registrar Blueprint
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, allow_unsafe_werkzeug=True)
