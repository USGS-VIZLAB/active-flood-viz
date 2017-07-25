var fs = require('fs');
var jsdom = require('jsdom/lib/old-api.js');
var data_hydro = require('./hydrograph_data.json');
var svg2png = require('svg2png');


jsdom.env(
	// create DOM hook
	"<html><body><div id='hydrograph'></div>" +
	"</body></html>",

	// load local assets into window environment (!)
	[
		'./floodviz/static/bower_components/d3/d3.js',
		'./floodviz/static/bower_components/jquery/dist/jquery.min.js',
		'./floodviz/static/js/hydro_thumbnail.js'
	],

	function (err, window) {

			var hydro_figure = window.thumbnail(
				{
					'height': 300,
					'width': 560,
					'div_id': '#hydrograph',
					'data': data_hydro,
					"hydrograph_display_ids": ['05471200', '05476750', '05411850', '05454220',
						'05481950', '05416900', '05464500', '05487470', '05457700', '05471000'] // Refactor Later
				}
			);

			hydro_figure.init(undefined);
			var svg = hydro_figure.svg_elem().node();
			var style = fs.readFileSync('floodviz/static/css/hydrograph.css', 'utf8');
			var svg_string = generate_style(style, svg);
			svg2png(svg_string)
				.then(buffer => fs.writeFile('figure.png', buffer));

			// Hook style to inline svg string.
			function generate_style(style_string, svgDomElement) {
				var s = window.document.createElement('style');
				s.setAttribute('type', 'text/css');
				s.innerHTML = "<![CDATA[\n" + style_string + "\n]]>";
				//somehow cdata section doesn't always work; you could use this instead:
				//s.innerHTML = styleDefs;
				var defs = window.document.createElement('defs');
				defs.appendChild(s);
				svgDomElement.insertBefore(defs, svgDomElement.firstChild);
				return svgDomElement.parentElement.innerHTML;
			}

	}
);




