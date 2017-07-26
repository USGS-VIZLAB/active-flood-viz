var fs = require('fs');
var jsdom = require('jsdom/lib/old-api.js');
var data_hydro = require('../static/data/hydrograph_data.json');
var data_map = require('../static/data/map_data.json');
var svg2png = require('svg2png');

jsdom.env(

	// create DOM hook
	"<html><body><div id='hydrograph'></div>" +
	"<div id='map'></divid>" +
	"</body></html>",

	// load local assets into window environment (!)
	[
		'./floodviz/static/bower_components/d3/d3.js',
		'./floodviz/static/bower_components/jquery/dist/jquery.min.js',
		'./floodviz/static/bower_components/proj4/dist/proj4.js',
		'./floodviz/posterioir_build/hydro_thumbnail.js',
		'./floodviz/posterioir_build/map_thumbnail.js'
	],

	function (err, window) {
		
			var map_figure = window.mapmodule(
				{
					'height': 300,
					'width': 560,
					'proj': window.proj4(data_map.proj4string),
					'bounds': data_map.bounds,
					'scale': data_map.scale,
					'bg_data': data_map.bg_data,
					'rivers_data': data_map.rivers_data,
					'ref_data': data_map.ref_data,
					'site_data': data_map.site_data,
					'div_id': '#map',
					'display_ids': ['05471200', '05476750', '05411850', '05454220',
                     '05481950', '05416900', '05464500', '05487470']
					// Refactor Later. I'm assuming this will change with refrences.json
				}
			);

			var hydro_figure = window.hydromodule(
				{
					'height': 300,
					'width': 560,
					'div_id': '#hydrograph',
					'data': data_hydro,
					"display_ids": ['05471200', '05476750', '05411850', '05454220',
                     '05481950', '05416900', '05464500', '05487470']
					// Refactor Later. I'm assuming this will change with refrences.json
				}
			);

			hydro_figure.init(undefined);
			var svg_h = hydro_figure.get_svg_elem().node();
			var style_h = fs.readFileSync('floodviz/static/css/hydrograph.css', 'utf8');
			var svg_string_h = generate_style(style_h, svg_h);
			// Takes care of canvas conversion
			svg2png(svg_string_h)
				.then(buffer => fs.writeFile('thumbnail_hydro.png', buffer))
				.then(console.log('\nConverted D3 hydrograph to PNG successfully... \n'))
				.catch(e => console.error(e));

			map_figure.init(undefined);
			var svg_m = map_figure.get_svg_elem().node();
			var style_m = fs.readFileSync('floodviz/static/css/map.css', 'utf8');
			var svg_string_m = generate_style(style_m, svg_m);
			// Takes care of canvas conversion
			svg2png(svg_string_m)
				.then(buffer => fs.writeFile('thumbnail_map.png', buffer))
				.then(console.log('\nConverted D3 map to PNG successfully... \n'))
				.catch(e => console.error(e));

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




