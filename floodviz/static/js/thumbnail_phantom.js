var fs = require('fs');
//var system = require('system');
var data_hydro = require('../data/hydrograph_data.json');
var page = require('webpage').create();
var url = 'file://' + fs.absolute('./floodviz/templates/thumbnail.html');

page.onConsoleMessage = function(msg) {
    system.stderr.writeLine('console: ' + msg);
};

page.open(url, data_hydro, function (status) {

	if (status === 'success') {
		page.injectJs('../bower_components/d3/d3.js');

		if (page.injectJs('hydro_thumbnail.js')){

			var hydro_thumbnail = page.evaluate(function (data_hydro) {

				var options = 	{
					'height': 200,
					'width': 200,
					'div_id': '#hydrograph',
					'data': data_hydro,
					"hydrograph_display_ids": ['05471200', '05476750', '05411850', '05454220',
						'05481950', '05416900', '05464500', '05487470', '05457700', '05471000'] // Refactor Later
				};

				var figure = thumbnail(options);
				figure.init(undefined);
				return figure.svg_string();
			}, data_hydro);

			//var string = hydro_thumbnail.svg_string();
			console.log(hydro_thumbnail);
			phantom.exit();
			// console.log(hydro_thumbnail.svg_string());
		}
	}
});
