from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1621@localhost/cumple'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

from sqlalchemy import CHAR, Column, Date, ForeignKey, String, TIMESTAMP, Text, text, BOOLEAN
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Client(db.Model):
    __tablename__ = 'clients'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), nullable=False)
    rut = Column(String(45), nullable=True)
    direccion = Column(String(45), nullable=True)
    website = Column(String(45), nullable=True)
    email = Column(String(45), nullable=True)
    phone = Column(String(45), nullable=True)  
    users_id = Column(ForeignKey('users.id'), nullable=True, index=True)

    users = relationship('User')
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rut": self.rut,
            "direccion": self.direccion,
            "website": self.website,
            "email":self.email,
            "phone":self.phone,
            "users_id":self.users_id
            

        }
class Country(db.Model):
    __tablename__ = 'countries'

    id = Column(INTEGER(11), primary_key=True)
    country = Column(String(45))  

    def serialize(self):
        return {
            "id": self.id,
            "country": self.country
        }

class Region(db.Model):
    __tablename__ = 'regions'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    region = Column(String(45))
    countries_id = Column(ForeignKey('countries.id'), primary_key=True, nullable=False, index=True)

    countries = relationship('Country')

    def serialize(self):
        return {
            "id": self.id,
            "region": self.region,
            "countries_id": self.countries_id
        }

class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(120))
    code = Column(String(6))
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
           
        }

class Typecontact(db.Model):
    __tablename__ = 'typecontact'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,

        }

class Typesrelative(db.Model):
    __tablename__ = 'typesrelatives'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,

        }

class Village(db.Model):
    __tablename__ = 'villages'

    id = Column(INTEGER(11), primary_key=True) # nullable=False cambiar
    village = Column(String(45))
    regions_id = Column(ForeignKey('regions.id'), primary_key=True, nullable=False, index=True)
    regions = relationship('Region')

    def serialize(self):
        return {
            "id": self.id,
            "village": self.village,
            "regions_id": self.regions_id,
        
        }

class Person(db.Model):
    __tablename__ = 'persons'
    id = Column(INTEGER(11), primary_key=True)
    national_id = Column(INTEGER(11))
    lastname = Column(String(45), nullable=False)
    name = Column(String(45), nullable=False)
    sex = Column(CHAR(3))
    birthday = Column(Date, nullable=False)
    address = Column(String(45))
    villages_id = Column(ForeignKey('villages.id'), nullable=False, index=True)

    villages = relationship('Village')


    def serialize(self):
        return {
            "id": self.id,
            "national_id": self.national_id,
            "lastname": self.lastname,
            "name": self.name,
            "sex": self.sex,
            "birthday": self.birthday,
            "address": self.address,
            "villages_id":self.villages_id
        }

class User(db.Model):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(45), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    create_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(TIMESTAMP)
    roles_id = Column(ForeignKey('roles.id'), nullable=False, index=True)

    roles = relationship('Role')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "roles_id": self.roles_id
        }



class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = Column(INTEGER(11), primary_key=True)
    endDate = Column(Date)
    budget = Column(INTEGER(10), nullable=False)
    villages_id = Column(ForeignKey('villages.id'), nullable=False, index=True)
    days_before = Column(INTEGER(11))
    sms = Column(String(30))
    mail = Column(Text)
    admin_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    client_id = Column(ForeignKey('users.id'), nullable=False, index=True)

    admin = relationship('User', primaryjoin='Campaign.admin_id == User.id')
    client = relationship('User', primaryjoin='Campaign.client_id == User.id')
    villages = relationship('Village')
    
    def serialize(self):
        return {
            "id": self.id,
            "endDate": self.endDate,
            "budget": self.budget,
            "villages_id": self.villages_id,
            "days_before": self.days_before,
            "sms": self.sms,
            "mail": self.mail,
            "admin_id": self.admin_id,
            "admin": self.admin,

        }



class Contact(db.Model):
    __tablename__ = 'contacts'

    id = Column(INTEGER(11), primary_key=True)
    data = Column(String(45))
    typeContact_id = Column(ForeignKey('typecontact.id'), nullable=False, index=True)
    Persons_id = Column(ForeignKey('persons.id'), nullable=False, index=True)

    Persons = relationship('Person')
    typeContact = relationship('Typecontact')

    def serialize(self):
        return {
            "id": self.id,
            "data": self.data,
            "typeContact_id": self.typeContact_id,
            "Persons_id": self.Persons_id,

        }



class Family(db.Model):
    __tablename__ = 'families'

    id = Column(INTEGER(11), primary_key=True)
    typesRelatives_id = Column(ForeignKey('typesrelatives.id'), nullable=False, index=True)
    Persons_id = Column(ForeignKey('persons.id'), nullable=False, index=True)
    Relative_id = Column(ForeignKey('persons.id'), nullable=False, index=True)

    Persons = relationship('Person', primaryjoin='Family.Persons_id == Person.id')
    Relative = relationship('Person', primaryjoin='Family.Relative_id == Person.id')
    typesRelatives = relationship('Typesrelative')

    def serialize(self):
        return {
            "id": self.id,
            "typesRelatives_id": self.typesRelatives_id,
            "Persons_id": self.Persons_id,
            "Relative_id": self.Relative_id,

        }    

class Report(db.Model):
    __tablename__ = 'reports'

    id = Column(INTEGER(11), primary_key=True)
    persons_id = Column(ForeignKey('persons.id'), nullable=False, index=True)
    campaigns_id = Column(ForeignKey('campaigns.id'), nullable=False, index=True)
    email_sent = Column(BOOLEAN(4)) #ANTES ERA TINYINT
    sms_sent = Column(BOOLEAN(4))

    campaigns = relationship('Campaign')
    persons = relationship('Person')

    def serialize(self):
        return {
            "id": self.id,
            "persons_id": self.persons_id,
            "campaigns_id": self.campaigns_id,
            "email_sent": self.email_sent,
            "sms_sent": self.sms_sent,            

        }      
