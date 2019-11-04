from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1621@localhost/cumple'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

from sqlalchemy import CHAR, Column, Date, ForeignKey, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Client(db.Model):
    __tablename__ = 'clients'

    id = Column(INTEGER(11), primary_key=True)
    rol_id = Column(String(45), nullable=False)

class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(120))
    code = Column(String(6))

class Status(db.Model):
    __tablename__ = 'status'

    id = Column(INTEGER(11), primary_key=True)
    Clients_User = Column(INTEGER(11), nullable=False)
    status = Column(String(45), nullable=False)

class Typecontact(db.Model):
    __tablename__ = 'typecontact'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))

class Typesrelative(db.Model):
    __tablename__ = 'typesrelatives'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), nullable=False)

class Village(db.Model):
    __tablename__ = 'villages'

    id = Column(INTEGER(11), primary_key=True)

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
            "address": self.address

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

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    days_before = Column(INTEGER(11))
    Log_in_User = Column('Log-in_User', String(45), nullable=False)
    sms = Column(String(30))
    mail = Column(Text)
    villages_id = Column(ForeignKey('villages.id'), nullable=False, index=True)
    Clients_User = Column(ForeignKey('clients.id'), nullable=False, index=True)
    users_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    status_id = Column(ForeignKey('status.id'), primary_key=True, nullable=False, index=True)

    client = relationship('Client')
    status = relationship('Status')
    users = relationship('User')
    villages = relationship('Village')


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = Column(INTEGER(11), primary_key=True)
    data = Column(String(45))
    typeContact_id = Column(ForeignKey('typecontact.id'), nullable=False, index=True)
    Persons_id = Column(ForeignKey('persons.id'), nullable=False, index=True)

    Persons = relationship('Person')
    typeContact = relationship('Typecontact')


class Family(db.Model):
    __tablename__ = 'families'

    id = Column(INTEGER(11), primary_key=True)
    typesRelatives_id = Column(ForeignKey('typesrelatives.id'), nullable=False, index=True)
    Persons_id = Column(ForeignKey('persons.id'), nullable=False, index=True)
    Relative_id = Column(ForeignKey('persons.id'), nullable=False, index=True)

    Persons = relationship('Person', primaryjoin='Family.Persons_id == Person.id')
    Relative = relationship('Person', primaryjoin='Family.Relative_id == Person.id')
    typesRelatives = relationship('Typesrelative')
