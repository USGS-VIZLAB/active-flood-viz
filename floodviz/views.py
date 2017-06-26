from flask import request, render_template, abort

from . import app
from . import maputils

@app.route('/home/')
def home():
    return render_template('index.html')

