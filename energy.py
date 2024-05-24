from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route('/')
def render_about():
    return render_template('intro.html')

    
@app.route('/commercial')
def commercial():
	with open('energy.json') as energy_data:
		weeks = json.load(energy_data)
	if 'year' in request.args:
		year = int (request.args['year'])
		state = request.args['state']
		return render_template('commercial.html', state_options = get_states_options(weeks), year_options = get_year_options(weeks), fuel = fuel(state, year, weeks, "Commercial")) 
	return render_template('commercial.html', state_options = get_states_options(weeks), year_options = get_year_options(weeks)) 
    
def fuel(state, year, data, sector):
	for d in data:
		if d["Year"] == year and d["State"] == state:
			html = Markup("<h2> " + state + " " + str(year) + "</h2><ul>")
			for source in d["Consumption"][sector]:
				html += Markup("<li>" + source + " " + str(d["Consumption"][sector] [source]) + "billion BTU </li>")
			html += Markup("</ul>")
			return html
    
@app.route('/residential')

def global_fuels():
	with open('energy.json') as energy_data:
		years = json.load(energy_data)
	if 'year' in request.args:
		year = int (request.args['year'])
		state = request.args['state']
		return render_template('residential.html', state_options = get_states_options(years), year_options = get_year_options(years), fuel = fuel(state, year, years, "Residential")) 
	return render_template('residential.html', state_options = get_states_options(years), year_options = get_year_options(years))
    
@app.route('/transportation')
def expenditures():
	with open('energy.json') as energy_data:
		years = json.load(energy_data)
	if 'year' in request.args:
		year = int (request.args['year'])
		state = request.args['state']
		return render_template('transportation.html', state_options = get_states_options(years), year_options = get_year_options(years), fuel = fuel(state, year, years, "Transportation")) 
	return render_template('transportation.html', state_options = get_states_options(years), year_options = get_year_options(years))
     
@app.route('/industrial')
def environment():
	with open('energy.json') as energy_data:
		years = json.load(energy_data)
	if 'year' in request.args:
		year = int (request.args['year'])
		state = request.args['state']
		return render_template('industrial.html', state_options = get_states_options(years), year_options = get_year_options(years), fuel = fuel(state, year, years, "Industrial")) 
	return render_template('industrial.html', state_options = get_states_options(years), year_options = get_year_options(years))
    
def get_year_options(data):
		years=[]
		options=""
		for d in data:
			year = d["Year"]
			if (year not in years):
				years.append(year)
				options += Markup("<option value=\"" + str(year) + "\">" + str(year) + "</option>")
		return options
    	
    	
def get_states_options(data):
		states=[]
		options=""
		for d in data:
			state = d["State"]
			if (state not in states):
				states.append(state)
				options += Markup("<option value=\"" + str(state) + "\">" + str(state) + "</option>")
		return options



def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url


if __name__ == '__main__':
    app.run(debug=False) # change to False when running in production
