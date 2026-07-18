import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "clave_secreta_academymap_2026"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database", "academy.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False