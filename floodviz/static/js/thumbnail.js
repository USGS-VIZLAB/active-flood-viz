// Run me with and pass me variables:
// $ WIDTH=800 ITEM="world-1e3" node mapIt.node.js
/* ***************************************************************** */
//Nodejs code:
var jsdom = require('jsdom/lib/old-api.js');  		// npm install jsdom
var fs = require('fs'); 			// natively in nodejs.

jsdom.env(

		"<html><body><div id='hydrograph'></div></body></html>",     // CREATE DOM HOOK
		// load assets into window environment (!)
		["{{ url_for('static', filename='bower_components/d3/d3.js') }}",
			"{{ url_for('static', filename='bower_components/jquery/dist/jquery.min.js') }}",
			"{{ url_for('static', filename='js/hydrograph.js')}}"
		],

		function (err, window) {
			/* ***************************************************************** */
			/* Check availability of loaded assets in window scope. ************ */
			console.log(typeof window.hydromodule);       // expect: 'function',  because exist in script.js !
			console.log(typeof window.doesntExist);

			/* ***************************************************************** */
			/* D3js FUNCTION *************************************************** */
			var hydro_figure = window.hydromodule(
				{'height': FV.hydrograph_dimensions.height,
					'width': FV.hydrograph_dimensions.width,
					'div_id': '#hydrograph',
				}
			);
			hydro_figure.init();

			/* ***************************************************************** */
			/* SVG PRINT ******************************************************* */
			setTimeout(
				function () {
					fs.writeFileSync('hydrograph.svg', window.d3.select("body").html());
				},
				7000
			);
		}
);

