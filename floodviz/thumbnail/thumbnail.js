/*
*
* This Script is intended to be run after a flask freeze during the build process.
*
* Its main objective is to dynamically create thumbnails for the site figures
* based on the data obtained from our server side flask services.
*
*
*/

// Dependency Import
var fs = require('fs');
var jsdom = require('jsdom/lib/old-api.js');
var svg2png = require('svg2png');
// Data imports
var data_hydro = require('../thumbnail/hydrograph_data.json');
var reference = require('../../instance/reference.json');

// Collect script arguments for external css
var style_ext = null;
var args = process.argv.splice(process.execArgv.length + 2);

if (args.length > 2) {
	console.log('\nUsage: node thumbnail.js ' +
		'\n\nOptional flag: -css path/to/css/file.css\n');
	process.exit();
} else {
	if (args[0]) {
		if (args[0] === '-css') {
			try {
				style_ext = fs.readFileSync(args[1], 'utf8');
			} catch(error) {
				console.log('\nError: external css file path not found. - Using only default style.\n\n' + error);
				style_ext = null;
			}
		} else {
			console.log('\nUnrecognized argument: ' + args[0]);
			console.log('\nUsage: node thumbnail.js ' +
				'\n\nOptional flag: -css path/to/css/file.css\n');
			process.exit();
		}
	}
}

var height = 300;
var width = 560;


// Headless Browser Start for DOM
jsdom.env(

	// create DOM hook
	"<html><body><div id='hydrograph'></div>" +
	"</body></html>",

	// load local assets into window environment
	[
		'./floodviz/static/bower_components/d3/d3.js',
		'./floodviz/static/js/hydrograph.js'
	],

	function (err, window) {
		var hydro_figure = window.hydromodule(
			{
				'height': height,
				'width': width,
				'div_id': '#hydrograph',
				"display_ids": reference.display_sites
			}
		);
		convert(hydro_figure,window, 'floodviz/static/css/hydrograph.css', 'floodviz/thumbnail/thumbnail_hydro.png');
	}
);

// Wrapper around svg2png that injects custom css to inline svg before conversion
function convert(figure, window, css_path, filename) {
	var style_ext = null;
	var svg_string = null;
	var svg = figure.get_svg_elem().node();
	var style_default = fs.readFileSync(css_path, 'utf8');
	figure.init(null, data_hydro);
	svg_string = inject_style(style_default, style_ext, svg, window);
	// Takes care of canvas conversion and encodes base64
	svg2png(svg_string, {height: height, width: width})
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
