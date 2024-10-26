from flask import Flask
from flask_cors import CORS
from routes import main_blueprint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Registrar Blueprint
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
