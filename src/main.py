"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, redirect
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
#from flask import Response
from utils import APIException, generate_sitemap
from models import db

from flask_mail import Mail, Message

from passlib.hash import pbkdf2_sha256 as sha256 #PASOXXX

from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity)

from models import Person
from models import Client
from models import Role
from models import User
from models import Campaign
from models import Contact
#from models import * para traer todas las tablas y despues llamarlas  models.Person



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY') #PASOYYY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 #PASOYYY

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tareas4geeks@gmail.com'
app.config['MAIL_PASSWORD'] = '4geeks2019'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
jwt = JWTManager(app)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#@app.route('/hello', methods=['POST', 'GET'])
#    def handle_person():
#
 #   response_body = {
  #      "hello": "world"
   # }

   # return jsonify(response_body), 200

@app.route('/register', methods=['POST']) #PASOXXX
def handle_register():

    data = request.json
    user = User() #PASOXXX
    usuarioexiste = User.query.filter_by(username=data["username"]).first()
    if usuarioexiste is not None:
        return jsonify({
            "ERROR": "USUARIO YA EXISTE"
        }), 200
    user.username = data["username"]
    user.password = sha256.hash(data["password"])
    user.roles_id = data["roles_id"] 
    #respuesta=user.serialize()
    db.session.add(user) #PASOXXX
    db.session.commit()

    return jsonify(user.serialize()), 200

@app.route('/login', methods=['POST'])
def handle_login():
    data = request.json
   # Response(headers={'Access-Control-Allow-Origin':'*'})
    all_people = User.query.filter_by(username=data["username"]).first() #PASOYYY
    if all_people is None:
        return jsonify({
            "ERROR": "USUARIO NO EXISTE"
        }), 200

    if sha256.verify(data["password"], all_people.password): ##PASOYYY
        MI = create_access_token(identity = data["username"])
        REFRESH = create_refresh_token(identity = data["username"])
        return jsonify({
            "token": MI,
            "refresh": REFRESH
            }), 200

    return jsonify({
            "ERROR": "LA CONTRASEÑA NO ES VALIDA"
        }), 200    


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

@app.route('/persons/<string:birthday>', methods=['GET'])
def handle_persona3(birthday):
    
    if request.method=='GET':
        personas= Person.query.filter_by(birthday=birthday)
        personas = list(map(lambda x: x.serialize(), personas))
        return jsonify(personas), 200 

@app.route('/village/<int:villages_id>', methods=['POST'])
def handle_persona4(villages_id):
    if request.method=='POST':
        data = request.json
        personas= Person.query.filter_by(villages_id=villages_id,birthday="18/01/08")
        #personas= personas.query.filter_by(birthday=data['days_before'])        
        contactos=Contact.query.filter_by(Persons_id=9)
        
        mail = Mail(app)
        msg = Message('Hello',
            sender = 'tareas4geeks@gmail.com',
            recipients = ['simon.larah@gmail.com','sotomayor001@gmail.com','jorge_raggio_a@hotmail.com']

        )
        msg.subject = 'FELIZ CUMPLEAÑOS! te desea Pastelería Las Delicias'
        msg.html = data['mail']
        mail.send(msg)

        personas = list(map(lambda x: x.serialize(), personas))
        contactos = list(map(lambda x: x.serialize(), contactos))
        return jsonify(contactos), 200     

@app.route('/clients', methods=['GET'])
#@jwt_required
def clientes():
    
    if request.method=='GET':
        
        clients = Client.query.all()
        clients = list(map(lambda x: x.serialize(), clients))
       
        return jsonify(clients), 200

@app.route('/clients', methods=['POST'])
def clientes2():
    
    data = request.json
    client = Client() #PASOXXX
    clienteexiste = Client.query.filter_by(rut=data["rut"]).first()
    if clienteexiste is not None:
        return jsonify({
            "ERROR": "RUT DE CLIENTE YA EXISTE"
        }), 200    
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

@app.route('/clients/<int:id>', methods=['DELETE'])
#@jwt_required
def clientsDelete(id):

    client = Client()
    client = Client.query.filter_by(id=id).first()
    borrado=client
    db.session.delete(client) #PASOXXX
    db.session.commit()

    return jsonify('borrado cliente'), 200    

@app.route('/campaigns/<int:client_id>', methods=['GET'])
def handleCampaigns(client_id):
    
    if request.method=='GET':
        campaigns= Campaign.query.filter_by(client_id=client_id)
        campaigns = list(map(lambda x: x.serialize(), campaigns))
        return jsonify(campaigns), 200  

@app.route('/campaigns/<int:id>', methods=['DELETE'])
#@jwt_required
def campaignDelete(id):

    campaign = Campaign()
    campaign = Campaign.query.filter_by(id=id).first()
    borrado=campaign
    db.session.delete(campaign) #PASOXXX
    db.session.commit()

    return jsonify('Campaña borrada'), 200            

@app.route('/campainsAdd', methods=['POST'])
def campainsAdd():
    
    data = request.json
    campaign = Campaign() #PASOXXX
    campaign.endDate = data["endDate"]
    campaign.budget = data["budget"]
    campaign.villages_id = data["villages_id"]
    campaign.days_before = data["days_before"]
    campaign.sms = data["sms"]
    campaign.mail = data["mail"]
    campaign.admin_id = data["admin_id"]
    campaign.client_id = data["client_id"]
    #user.password = sha256.hash(data["password"])
    db.session.add(campaign) #PASOXXX
    db.session.commit()

    return jsonify(campaign.serialize()), 200


@app.route('/roles')
def GetRoles():
    
    roles = Role.query.all()
    roles = list(map(lambda x: x.serialize(), roles))

    return jsonify(roles), 200        


@app.route('/roles', methods=['POST'])
def postRoles():
    
    data = request.json
    rol = Role() #PASOXXX
    rol.name = data["name"]
    rol.code = data["code"]

    db.session.add(rol) #PASOXXX
    db.session.commit()

    return jsonify(rol.serialize()), 200    


@app.route('/users', methods=['POST'])
def postUsers():
    
    data = request.json
    user = User() #PASOXXX
    user.username = data["username"]
    user.password = data["password"]
    user.create_at = data["create_at"]
    user.update_at = data["update_at"]
    user.roles_id = data["roles_id"]

    db.session.add(user) #PASOXXX
    db.session.commit()

    return jsonify(user.serialize()), 200   


@app.route('/users',methods=['GET'])
    
def GetUsers():
    
    users = User.query.all()
    users = list(map(lambda x: x.serialize(), users))

    return jsonify(users), 200    

@app.route('/test-mail', methods=['POST'])

def sendmail():
    data = request.json
    mail = Mail(app)
    msg = Message('Hello',
        sender = 'tareas4geeks@gmail.com',
        recipients = data['recipients'],

    )
    msg.subject = 'FELIZ CUMPLEAÑOS!'
    msg.html = data['html']
    mail.send(msg)


    return jsonify('mail enviado'), 200









# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
