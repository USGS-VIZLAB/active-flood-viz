from flask import request, render_template, abort

from . import app

@app.route('/home/')
def home():
    return render_template('index.html')

