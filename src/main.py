"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Person
from models import Client
#from models import * para traer todas las tablas y despues llamarlas  models.Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_person():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route('/persons', methods=['GET'])
def handle_persona():
    

        
    persons = Person.query.all()
    persons = list(map(lambda x: x.serialize(), persons))
       
    return jsonify(persons), 200

@app.route('/persons/<int:national_id>', methods=['GET'])
def handle_persona2(national_id):
    
    if request.method=='GET':
        persona = Person.query.filter_by(national_id=national_id).first().serialize()
        #personas = Person.query.filter_by(national_id=national_id)
        #persona = list(map(lambda x: x.serialize(), personas))
        return jsonify(persona), 200

#@app.route('/persons/<int:birthday>')
#def handle_persona3(birthday):
    
   # if request.method=='GET':
   #     person= person.querry.filterBy(birthday='birthday')
   #     return jsonify(person), 200 

#@app.route('/persons/<int:villages_id>')
#def handle_persona4(villages_id):
    #pass

@app.route('/clients', methods=['GET'])
def clientes():
    
    if request.method=='GET':
        
        clients = Client.query.all()
        clients = list(map(lambda x: x.serialize(), clients))
       
        return jsonify(clients), 200

@app.route('/clients', methods=['POST'])
def clientes2():
    
    data = request.json
    client = Client() #PASOXXX
    client.name = data["name"]
    client.rut = data["rut"]
    client.direccion = data["direccion"]
    client.website = data["website"]
    client.email = data["email"]
    client.phone = data["phone"]
    client.users_id = data["users_id"]
    #user.password = sha256.hash(data["password"])
    db.session.add(client) #PASOXXX
    db.session.commit()

    return jsonify(client.serialize()), 200

# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
