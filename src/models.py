from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    national_id = db.Column(db.Integer, unique=True, nullable=True)
    lastName = db.Column(db.String(80), nullable=True)
    names = db.Column(db.String(80),  nullable=False)
    sex = db.Column(db.String(3),  nullable=False)
    birthday = db.Column(db.Date,  nullable=False)
    #address = db.Column(db.String(100),  nullable=False)
    village_id = db.Column(db.Integer,nullable=False)
    
    def __repr__(self):
        return '<Persons %r>' % self.id

    def serialize(self):
        return {
             "id": self.id,
             "national_id": self.national_id,
             "lastName": self.emlastNameail,
             "names": self.names,
             "sex": self.sex,
             "birthday": self.birthday,
             "village_id": self.village_id
        }