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

			d3.select('#peakflow_bar svg').datum(data).call(chart);

			// TODO: custom D3 for lollipop! -- figure out how to make cx and cy dynamic. CY is close... -> https://developer.mozilla.org/en-US/docs/Web/API/SVGLength#Example
			var bars = d3.select('#peakflow_bar svg').selectAll('.nv-bar')[0];
			var lolli = bars[bars.length-1];
			lolli.setAttribute("id", "lollipop");
			var cy = lolli.y.baseVal;
			var cx = lolli.x.baseVal;
			console.log(cy, cx);
			cy.convertToSpecifiedUnits(2);
			cx.convertToSpecifiedUnits(2);
			console.log(cy.valueInSpecifiedUnits);
			console.log(cx.valueInSpecifiedUnits);
			var group = d3.select('#peakflow_bar .nv-series-0');
			group.append("circle").attr('r', "10").attr('cx', cx.valueInSpecifiedUnits ).attr('cy', cy.valueInSpecifiedUnits);


			nv.utils.windowResize(chart.update);
			return chart;
		});
	});
});