from flask import Flask, request, jsonify

app = Flask(__name__);

@app.route('/up', methods=['GET'])
def up():
    return jsonify({"status": "up"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
