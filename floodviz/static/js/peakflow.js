document.addEventListener("DOMContentLoaded", function(event) { 

	"use strict";

	// Collect and set peakflow bar chart aspect ratio data
	var peakflow_bar = document.getElementById('peakflow_bar');
	peakflow_bar.style.height = FV.peakmeta['height'];
	peakflow_bar.style.width = FV.peakmeta['width'];

	d3.json('../static/data/peak_flow_data.json', function(data) {

		nv.addGraph(function() {
			
			var chart = nv.models.multiBarChart()
				.x( function(d) { return d.label; })
				.y( function(d) { return d.value; })
				.reduceXTicks(true)
				.showControls(false)
				.margin({left: 100, top: 100})
				.groupSpacing(.01);

			chart.xAxis.axisLabel(" Year ");

			chart.yAxis.axisLabel(" Peak Annual Flow (cfps)")
				.axisLabelDistance(20);

			// TODO: custom D3 for lollipop!
			var bars = d3.selectAll("#peakflow_bar rect");
			console.log(bars);

			


			d3.select('#peakflow_bar svg').datum(data).call(chart);
			nv.utils.windowResize(chart.update);
			return chart;
		});
	});
});