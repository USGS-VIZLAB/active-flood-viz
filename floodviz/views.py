from flask import request, render_template, abort #, jsonify

## below is for data processing ##
import json
import time
from datetime import datetime
import requests
# # # # # # # # # # # # # # # # # #

from . import app

@app.route('/home/')
def home():
  	## new data store ##
	newd = []
	
	# TODO: Figure out a better way to do this parameter(site, start, end) collection
	sites = ['05463500', '05471050', '05420680']#, '05479000', '05484000', '05481000', '05486000', '05421000', '05485500', '05455100', '05470500', '05451500']
	start_date = '2008-05-20'
	end_date = '2008-07-05'
	# # Do this betta  ^ # #
	

	## Set up to retrieve all site ids from url? ##
	for idx, site in enumerate(sites):
		url = 'https://nwis.waterservices.usgs.gov/nwis/iv/?site=' + site + '&startDT=' + start_date + '&endDT=' + end_date + '&parameterCD=00060&format=json'
		#print(url)
		r = requests.get(url)
		if r.status_code is 200:
			j = r.json()
			key = site # Key for this series
			newd.append({'key': key, 'values': []})
			# Fill new data
			for idx2, obj in enumerate(j['value']['timeSeries'][0]['values'][0]['value']):
				value = obj['value']
				dt = obj['dateTime']
				date = dt.split('T')[0]
				t = dt.split('T')[1].split('.')[0]
			 	# reformat datetime for python datetime
				dt = datetime.strptime(date + ' ' + t, '%Y-%m-%d %H:%M:%S')
				# Conver to miliseconds for use with d3 axis format
				dt_ms = time.mktime(dt.timetuple()) * 1000
				newd[idx]['values'].append({'date':date, "time": t, "time_mili": dt_ms, 'value': value})

	
	with open('floodviz\static\data\hydrograph_data.json', 'w') as fout:		# TODO: More dynamic file path
		json.dump(newd, fout, indent=1)

	return render_template('index.html')
	# return render_template('index.html', datahydro=json.dumps(newd))
	######## For passing json as object to client javascript. (d3 needs a json file though)