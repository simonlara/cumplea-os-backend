from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1621@localhost/cumple'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from sqlalchemy import CHAR, Column, DECIMAL, Date, ForeignKey, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Country(Base):
    __tablename__ = 'countries'

    id = Column(INTEGER(11), primary_key=True)
    country = Column(String(45))


class Role(Base):
    __tablename__ = 'roles'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(120))
    code = Column(String(6))


class Typecontact(Base):
    __tablename__ = 'typecontact'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))


class Typesrelative(Base):
    __tablename__ = 'typesrelatives'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), nullable=False)


class Region(Base):
    __tablename__ = 'regions'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    region = Column(String(45))
    countries_id = Column(ForeignKey('countries.id'), primary_key=True, nullable=False, index=True)

    countries = relationship('Country')


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(45), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    create_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(TIMESTAMP)
    roles_id = Column(ForeignKey('roles.id'), nullable=False, index=True)

    roles = relationship('Role')

class Client(Base):
    __tablename__ = 'clients'

    id = Column(INTEGER(11), primary_key=True)
    nombre = Column(String(45))
    rut = Column(String(45))
    direccion = Column(String(45))
    website = Column(String(45))
    email = Column(String(45))
    phone = Column(String(45))
    users_id = Column(ForeignKey('users.id'), nullable=False, index=True)

    users = relationship('User')


class Village(Base):
    __tablename__ = 'villages'

    id = Column(INTEGER(11), primary_key=True, nullable=False)
    village = Column(String(45))
    regions_id = Column(ForeignKey('regions.id'), primary_key=True, nullable=False, index=True)

    regions = relationship('Region')


class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(INTEGER(11), primary_key=True)
    endDate = Column(Date)
    budget = Column(DECIMAL(10, 0), nullable=False)
    villages_id = Column(ForeignKey('villages.id'), nullable=False, index=True)
    days_before = Column(INTEGER(11))
    sms = Column(String(30))
    mail = Column(Text)
    admin_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    client_id = Column(ForeignKey('users.id'), nullable=False, index=True)

    admin = relationship('User', primaryjoin='Campaign.admin_id == User.id')
    client = relationship('User', primaryjoin='Campaign.client_id == User.id')
    villages = relationship('Village')


class Person(Base):
    __tablename__ = 'persons'

    id = Column(INTEGER(11), primary_key=True)
    national_id = Column(INTEGER(11))
    lastname = Column(String(45), nullable=False)
    name = Column(String(45), nullable=False)
    sex = Column(CHAR(3))
    birthday = Column(Date, nullable=False)
    address = Column(String(45))
    villages_id = Column(ForeignKey('villages.id'), index=True)

    villages = relationship('Village')


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(INTEGER(11), primary_key=True)
    data = Column(String(45))
    typeContact_id = Column(ForeignKey('typecontact.id'), nullable=False, index=True)
    Persons_id = Column(ForeignKey('persons.id'), nullable=False, index=True)

    Persons = relationship('Person')
    typeContact = relationship('Typecontact')


class Family(Base):
    __tablename__ = 'families'

    id = Column(INTEGER(11), primary_key=True)
    typesRelatives_id = Column(ForeignKey('typesrelatives.id'), nullable=False, index=True)
    Persons_id = Column(ForeignKey('persons.id'), nullable=False, index=True)
    Relative_id = Column(ForeignKey('persons.id'), nullable=False, index=True)

    Persons = relationship('Person', primaryjoin='Family.Persons_id == Person.id')
    Relative = relationship('Person', primaryjoin='Family.Relative_id == Person.id')
    typesRelatives = relationship('Typesrelative')


class Report(Base):
    __tablename__ = 'reports'

    id = Column(INTEGER(11), primary_key=True)
    persons_id = Column(ForeignKey('persons.id'), nullable=False, index=True)
    campaigns_id = Column(ForeignKey('campaigns.id'), nullable=False, index=True)
    email_sent = Column(TINYINT(4))
    sms_sent = Column(TINYINT(4))

    campaigns = relationship('Campaign')
    persons = relationship('Person')