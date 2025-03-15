from flask import Flask
from fastapi import FastAPI

flask_app = Flask(__name__, template_folder="templates", static_folder="static")
fastapi_app = FastAPI()
