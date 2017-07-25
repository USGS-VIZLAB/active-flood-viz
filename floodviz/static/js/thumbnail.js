var jsdom = require('jsdom/lib/old-api.js');
var fs = require('fs');
var exportSVG = require('export-svg-chart');
var data_hydro = require('./hydrograph_data.json');


jsdom.env(
	// create DOM hook
	"<html><body><div id='hydrograph'></div>" +
	"</body></html>",

	// load local assets into window environment (!)
	[
		'./floodviz/static/bower_components/d3/d3.js',
		'./floodviz/static/bower_components/jquery/dist/jquery.min.js',
		'./floodviz/static/js/hydro_thumbnail.js',
		'./floodviz/static/css/hydrograph.css'
	],

	function (err, window) {

			var hydro_figure = window.thumbnail(
				{
					'height': 200,
					'width': 200,
					'div_id': '#hydrograph',
					'data': data_hydro,
					"hydrograph_display_ids": ['05471200', '05476750', '05411850', '05454220',
						'05481950', '05416900', '05464500', '05487470', '05457700', '05471000'] // Refactor Later
				}
			);

			hydro_figure.init(undefined);
			var svg_string = hydro_figure.svg_string();

	}
);




