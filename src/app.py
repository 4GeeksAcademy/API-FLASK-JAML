"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify({"success": True, "family": members}), 200


@app.route('/members/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify({"success": True, "member": member}), 200
    else:
        return jsonify({"success": False, "message": "No se encontro el miembro de la familia"}), 404
    
@app.route('/add', methods=['POST'])
def add_member():
    data = request.json
    new_member = jackson_family.add_member(data)
    return jsonify({"success": True, "new_member": new_member}), 201

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    deleted = jackson_family.delete_member(id)
    if deleted:
        return jsonify({"success": True, "message": f"Miembro con id {id} eliminado"}), 200
    else:
        return jsonify({"success": False, "message": "Miembro no encontrado"}), 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
