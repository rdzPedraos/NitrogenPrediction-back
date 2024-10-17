from flask import jsonify

from . import main_blueprint

@main_blueprint.route('/up', methods=['GET'])
def up():
    return jsonify({'status': 'up'}), 200
