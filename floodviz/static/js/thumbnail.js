
var jsdom = require('jsdom/lib/old-api.js');
var fs = require('fs');

var data_hydro = require('./hydrograph_data.json');

jsdom.env(
	"<html><body><div id='hydrograph'></div><script></script></body></html>",     // CREATE DOM HOOK

	// load assets into window environment (!)
	[
		'./floodviz/static/bower_components/d3/d3.js',
		'./floodviz/static/bower_components/jquery/dist/jquery.min.js',
		'./floodviz/static/js/hydro_thumbnail.js',
	],

	function (err, window) {
		var hydro_figure = window.thumbnail(
			{
				'height': 200,
				'width': 200,
				'div_id': '#hydrograph',
				'data': data_hydro,
				"site_display_ids": ['05471200', '05476750', '05411850', '05454220',
                     '05481950', '05416900', '05464500', '05487470']
			}
		);

		hydro_figure.init(undefined);

		// PRINT THAT SVG
		setTimeout(
			function () {
				fs.writeFileSync('hydrograph_thumbnail.svg', window.d3.select("body").html());
			},
			7000
		);
	}
);



