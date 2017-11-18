from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def render_home():
    return render_template('home.html')

@app.route('/map')
def render_map():
	return render_template('worldmap.html')

@app.route('/map-temp')
def render_map_temp():
	return render_template('worldMapPage.html')

@app.route('/login')
def render_login():
	return render_template('login.html')