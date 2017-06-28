document.addEventListener("DOMContentLoaded", function(event) { 

	"use strict";

	// Collect and set hydrograph aspect ratio data
	var hydrograph = document.getElementById('hydrograph');
	hydrograph.style.height = FV.hydrometa['height'];
	hydrograph.style.width = FV.hydrometa['width'];

	// D3 data import
	d3.json('../static/data/hydrograph_data.json', function(data) {

		nv.addGraph( function() {
			
			var getX = function(d) { return d.time_mili };
			var getY = function(d) { return d.value };
			
			// might want to switch to lineChart(). When cumulative line chart is clicked, the Y axis freaks out and reverts back to issue at https://github.com/novus/nvd3/issues/695 # 
			var chart = nv.models.cumulativeLineChart()
					.x( getX )  // this value is stored in milliseconds since epoch (converted in data_format.py with datetime)
					.y( getY ) 
					.color(d3.scale.category10().range())
					.useInteractiveGuideline(true)
					.yScale(d3.scale.log())	// Logarithmic Y axis. (GM - I think this make the flood event less decipherable in the visual but it probably scales better)
					.margin({left: 120, top: 60})
					.showLegend(false)
					.showControls(false);

			chart.xAxis.axisLabel(" Date (M-D-Y)")
					.axisLabelDistance(10)
					.ticks(5)
					.tickFormat(function(d){return d3.time.format('%m-%d-%y')(new Date(d))});

			chart.yAxis.axisLabel('Discharge (cubic feet per second)')
					.axisLabelDistance(40)
					.tickValues([10, 100, 1000, 10000, 100000])
					.tickFormat(function(d) { return d3.format(",")(d) + " cfps"});
			
			d3.select('#hydrograph svg').datum(data).call(chart);

			nv.utils.windowResize(chart.update);
			return chart;
	
		});
	});
});

