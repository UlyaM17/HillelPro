from flask import Flask
from sqlalchemy import SQLAlchemy
from datetime import datetime
from pydantic import BaseModel
from datetime import date

app = Flask(__name__)


@app.route('/health')
def health_check():
    return '', 200


db = SQLAlchemy()


class AnimalModel(BaseModel):
    name: str
    breed: str
    birthdate: date
    photo_url: str
    age: int


class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    breed = db.Column(db.String(120), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)


def calculate_age(birthdate):
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


@app.route('/search/<name>')
def search_animal(name):
    animals = Animal.query.filter(Animal.name.ilike(f'%{name}%')).all()
    return [AnimalModel.model_config(animal).dict() for animal in animals]
