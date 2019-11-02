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
from models import Persons
persons=Persons()

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

@app.route('/persons')
def handle_persona():
    
    if request.method=='GET':
        
        personas=jsonify(persons.querry.get())
       
        return personas,200

@app.route('/persons/<int:national_id>')
def handle_persona(national_id):
    
    if request.method=='GET':
        person=jsonify( persons.querry.filterBy(national_id='national_id')
        return person,200

@app.route('/persons/<int:birthday>')
def handle_persona(birthday):
    
    if request.method=='GET':
         personas=jsonify( persons.querry.filterBy(birthday='birthday')
         return personas,200   

@app.route('/persons/<int:villages_id>')
def handle_persona(villages_id):
    
    if request.method=='GET':
        person=jsonify( persons.querry.filterBy(villages_id='villages_id')
        return person,200     

   

       


# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
