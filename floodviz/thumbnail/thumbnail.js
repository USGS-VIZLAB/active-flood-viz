// Dependency Import
var fs = require('fs');
var jsdom = require('jsdom/lib/old-api.js');
var svg2png = require('svg2png');
// Data imports
var data_hydro = require('../thumbnail/hydrograph_data.json');
var data_map = require('../thumbnail/map_data.json');


// Collect script arguments for figure decision
var target = null;
var style_path = null;

var args = process.argv.splice(process.execArgv.length + 2);
if (args.length < 1 || args.length > 3) {
	console.log('\nUsage: node thumbnail.js -figureName ' + '\n\nValid figure names: -map, -hydro' +
		'\n\nOptional flag: -css path/to/css/file.css\n');
	process.exit();
} else {
	if(args[0] === '-hydro') {
		target = 'hydro';
	} else if (args[0] === '-map'){
		target = 'map';
	} else {
		console.log('\nInvalid argument.\nValid figure names: -map, -hydro\n');
		process.exit();
	}
	if (args[1]) {
		style_path = args[2];
	}
}

// Headless Browser Start for DOM
jsdom.env(

	// create DOM hook
	"<html><body><div id='hydrograph'></div>" +
	"<div id='map'></divid>" +
	"</body></html>",

	// load local assets into window environment
	[
		'./floodviz/static/bower_components/d3/d3.js',
		'./floodviz/static/bower_components/proj4/dist/proj4.js',
		'./floodviz/thumbnail/hydro_thumbnail.js',
		'./floodviz/thumbnail/map_thumbnail.js'
	],

	function (err, window) {
			if (target === 'hydro') {
				var hydro_figure = window.hydromodule(
					{
						'height': 300,
						'width': 560,
						'div_id': '#hydrograph',
						'data': data_hydro,
						"display_ids": ['05471200', '05476750', '05411850', '05454220',
						 '05481950', '05416900', '05464500', '05487470']
						// Refactor Later. I'm assuming this will change with references.json
					}
				);
				convert(hydro_figure, window, 'floodviz/static/css/hydrograph.css', 'floodviz/thumbnail/thumbnail_hydro.png');
			} else if (target === 'map') {
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
						// Refactor Later. I'm assuming this will change with references.json
					}
				);
				convert(map_figure, window, 'floodviz/static/css/map.css', 'floodviz/thumbnail/thumbnail_map.png');
			}
	}
);

// Wrapper around svg2png that injects custom css to inline svg before conversion
function convert(figure, window, css_path, filename) {
	figure.init(undefined);
	var style_ext = null;
	var svg_string = null;
	var svg = figure.get_svg_elem().node();
	var style_default = fs.readFileSync(css_path, 'utf8');
	if (style_path !== null) {
		style_ext = fs.readFileSync(style_path, 'utf8');
		svg_string = inject_style(style_default, style_ext, svg, window);
	} else {
		svg_string = inject_style(style_default, null, svg, window);
	}
	// Takes care of canvas conversion and encodes base64
	svg2png(svg_string)
		.then(buffer => fs.writeFile(filename, buffer))
		.then(console.log('\nConverted D3 figure to PNG successfully... \n'))
		.catch(e => console.error(e));
}

// Hook style to inline svg string.
function inject_style(style_string, ext_style, svgDomElement, window) {
	var s = window.document.createElement('style');
	s.setAttribute('type', 'text/css');
	s.innerHTML = "<![CDATA[\n" + style_string + ext_style + "\n]]>";
	var defs = window.document.createElement('defs');
	defs.appendChild(s);
	svgDomElement.insertBefore(defs, svgDomElement.firstChild);
	return svgDomElement.parentElement.innerHTML;
}
