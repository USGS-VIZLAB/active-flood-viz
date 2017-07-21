
var jsdom = require('jsdom/lib/old-api.js');
var fs = require('fs');
const svg2png = require('svg2png');
var data_hydro = require('./hydrograph_data.json');


jsdom.env(

	// create DOM hook
	"<html><body><div id='hydrograph'></div>" +
	//"<script type='text/javascript' src='//canvg.github.io/canvg/rgbcolor.js'></script>" +
	//"<script type='text/javascript' src='//canvg.github.io/canvg/StackBlur.js'></script>" +
	//"<script type='text/javascript' src='//canvg.github.io/canvg/canvg.js'></script>" +
	"<canvas id='canvas' width='1000px' height='600px'></canvas>" +
	"</body></html>",

	// load local assets into window environment (!)
	[
		'./floodviz/static/bower_components/d3/d3.js',
		'./floodviz/static/bower_components/jquery/dist/jquery.min.js',
		//'./floodviz/static/bower_components/canvg/dist/canvg.js',
		//'./floodviz/static/bower_components/rgbcolor/index.js',
		//'./floodviz/static/bower_components/StackBlur/StackBlur.js',
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

		//window.canvg('canvas', svg_string, { ignoreMouse: true, ignoreAnimation: true });

		// save svg
		setTimeout(
			function () {
				fs.writeFileSync('hydrograph_thumbnail.svg', svg_string);
			},
			6000
		);

		//var canvas = window.document.getElementById('canvas');
		//var png = canvas.toDataURl('image/png');

		// fs.readFile('hydrograph_thumbnail.svg')
		// 	.then(svg2png)
		// 	.then(buffer = fs.writeFile('thumbnail.png', buffer))
		// 	.catch(e = console.error(e));
	}
);



