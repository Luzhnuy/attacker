from flask import Flask, request
import sys
import os

app = Flask(__name__)
port = 80

@app.route('/')
def index():
    return "OK"

app.run(host="0.0.0.0", port=port)