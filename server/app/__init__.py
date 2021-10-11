from flask import Flask, Blueprint


#Create flask instance
app = Flask(__name__)

from . import views
