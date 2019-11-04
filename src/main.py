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
    
    if request.method=='GET':
        
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
   
# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
