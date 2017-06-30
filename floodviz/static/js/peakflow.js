document.addEventListener("DOMContentLoaded", function(event) { 

	"use strict";

	// Collect and set peakflow bar chart aspect ratio data
	var peakflow_bar = document.getElementById('peakflow_bar');
	peakflow_bar.style.height = FV.peakmeta['height'];
	peakflow_bar.style.width = FV.peakmeta['width'];

	var margin = {bottom: 100, right: 120, left: 120, top: 150};
	var	width = parseInt(FV.peakmeta['width']);
	var	height = parseInt(FV.peakmeta['height']);

	var x = d3.scale.ordinal().rangeRoundBands([0, width], .15);
	var	y = d3.scale.linear().range([height, 0]);

	var xAxis = d3.svg.axis().scale(x).orient('bottom');
	var yAxis = d3.svg.axis().scale(y).orient('left').ticks(8);

	var svg = d3.select('#peakflow_bar').append('svg').attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")").attr('class', 'group');


	d3.json('../static/data/peak_flow_data.json', function(data) {
		
		// For custom Y axis ticks
		var ticks = []
		data.forEach( function(d, i){
		 	if (i % 4 === 0) {
		 		ticks.push(d.label);
		 	}
		})
		xAxis.tickValues(ticks);

		x.domain(data.map(function(d) {return d.label; }));
		y.domain([0, d3.max(data, function(d) {return d.value; })]);

		svg.append("g").attr('class', "axis axis--x").attr("transform", "translate(0," + height + ")").call(xAxis)
			.append("text")
			.attr("text-anchor", "middle")
			.attr("x", (width/2))
			.attr("y", 0 + (margin.bottom/2))
			.text("Year");
		svg.append("g").attr('class', "axis axis--y").call(yAxis)
			.append("text")
			.attr("text-anchor", "middle")
			.attr("transform", "rotate(-90)")
			.attr("x", 0 - (height/2))
			.attr("y", 0 - (margin.left/2))
			.text("Discharge (cfps)");
		svg.selectAll("bar").data(data).enter().append("rect")
			.attr('class', 'bar')
			.attr("x", function(d) {return x(d.label); })
			.attr("y", function(d) {return y(d.value); })
			.attr("width", x.rangeBand())
			.attr("height", function(d) {return height - y(d.value); });
		svg.append("text")
			.attr("x", (width/2))
			.attr("y", 0 - (margin.top / 2))
			.attr("text-anchor", "middle")
			.text("Peak Annual Discharge")

		// Lollipop 
		var bars = d3.select('#peakflow_bar svg').selectAll('.bar')[0];
		var lolli = bars[bars.length-1];
		lolli.setAttribute("id", "lollipop");
		var cy = lolli.y.baseVal;
		var cx = lolli.x.baseVal;
		var loli_width = lolli.width.baseVal.value;
		var cr = "20";
		cy.convertToSpecifiedUnits(5);
		cx.convertToSpecifiedUnits(5);
		var group = d3.select('#peakflow_bar svg .group');
		group.append("circle").attr('class', 'cir')
			.attr('r', cr)
			.attr('cx', cx.value + (loli_width/3.5) )
			.attr('cy', cy.value  + parseInt(cr));	//offset by circle radius
	});
});