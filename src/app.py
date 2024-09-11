"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


# create the jackson family object
jackson_family = FamilyStructure("Jackson")

john = {
    "first_name": "John",
    "last_name": jackson_family.last_name, #(para sea dinamico) 
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

jane = {
    "first_name": "Jane",
    "last_name": jackson_family.last_name,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

jimmy = {
    "first_name": "Jimmy",
    "last_name": jackson_family.last_name,
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(john)
jackson_family.add_member(jane)
jackson_family.add_member(jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def obtener_miembros():
    # this is how you can use the Family datastructure by calling its methods
    miembros = jackson_family.get_all_members() 
    return jsonify(miembros), 200

@app.route('/member/<int:miembro_id>', methods=['GET'])
def obtener_miembro(miembro_id):
    miembro = jackson_family.get_member(miembro_id)
    return jsonify(miembro), 200

@app.route('/member', methods= ['POST'])
def crear_miembro():
    nuevo_miembro= request.json
   
    jackson_family.add_member(nuevo_miembro)
    return jsonify({'done':"usuario ok"}), 200 
    

@app.route('/member/<int:member_id>', methods=['DELETE'])
def borrar_miembro(member_id):
    borrado= jackson_family.delete_member(member_id)
    if not borrado:
        return jsonify({"msg":"familiar no encontrado"}), 400
    return {"done": True}, 200








# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
