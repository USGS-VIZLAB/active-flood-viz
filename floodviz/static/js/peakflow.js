document.addEventListener("DOMContentLoaded", function(event) { 

	"use strict";

	// Collect and set peakflow bar chart aspect ratio data
	var peakflow_bar = document.getElementById('peakflow_bar');
	peakflow_bar.style.height = FV.peakmeta['height'];
	peakflow_bar.style.width = FV.peakmeta['width'];

	var margin = {bottom: 40, right: 40, left: 40, top: 75};
	var width = parseInt(FV.peakmeta['width']);
	var height = parseInt(FV.peakmeta['height']);
	var data = FV.peakinfo;

	var x = d3.scaleBand().rangeRound([0, width]).padding(.5);
	var	y = d3.scaleLinear().range([height, 0]);

	var xAxis = d3.axisBottom().scale(x);
	var yAxis = d3.axisLeft().scale(y).ticks(8);

	var svg = d3.select('#peakflow_bar').append('svg')
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")")
				.attr('class', 'group');

	var tooltip = d3.select("body")
		.append("div")
		.attr("class", "toolTip");
		
	// For custom X axis ticks
	var ticks = []
	data.forEach( function(d, i){
		if (i % 4 === 0) {
			ticks.push(d.label);
		}
	})
	xAxis.tickValues(ticks);

	x.domain(data.map( function(d) {return d.label; }));
	y.domain([0, d3.max(data, function(d) {return d.value; })]);

	svg.append("g").attr('class', "axis axis--x").attr("transform", "translate(0," + height + ")").call(xAxis)
		.append("text")
		.attr("text-anchor", "middle")
		.attr("x", (width / 2))
		.attr("y", 0 + (margin.bottom / 2))
		.text("Year");
	svg.append("g").attr('class', "axis axis--y").call(yAxis)
		.append("text")
		.attr("text-anchor", "middle")
		.attr("transform", "rotate(-90)")
		.attr("x", 0 - (height / 2))
		.attr("y", 0 - (margin.left / 2))
		.text("Discharge (cfps)");

	// Save last data point as lollipop
	var lolli_data = data[data.length - 1];
	// remove last data point for creating bars
	data = data.slice(0, data.length - 1);


	// Normal Bar value creation
	svg.selectAll("bar").data(data).enter().append("rect")
		.attr('class', 'bar')
		.attr("x", function(d) {return x(d.label); })
		.attr("y", function(d) {return y(d.value); })
		.attr("width", x.bandwidth())
		.attr("height", function(d) {return height - y(d.value); })
		// tooltip event
		.on("mousemove", function(d) {mouseover(tooltip, d, d3.event)})
		.on("mouseout", function() {mouseout(tooltip)});
	
	// var description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit";
	// svg.append("text")
	// 	.attr("x", (width/2))
	// 	.attr("y", height + 50)
	// 	.attr("text-anchor", "middle")
	// 	.text(description);

	// create lollipop Stroke and Circle
	var bars = d3.select('#peakflow_bar svg').selectAll('.bar')['_groups'][0];
	var last_bar = bars[bars.length-1];
	var penultimant_bar = bars[bars.length-2];
	var lb_x = last_bar.x.baseVal.value;
	var slb_x = penultimant_bar.x.baseVal.value;
	var padding = lb_x - slb_x;
	var lolli_pos_x = ((lb_x + padding + ((1/2) * x.bandwidth())).toString())
	var lolli_pos_y = (y(lolli_data['value'])).toString()
	var path_string = "M " + lolli_pos_x +"," + FV.peakmeta['height'] + " " + lolli_pos_x + "," + lolli_pos_y;
	svg.append("path")
		.attr('id', 'lollipop')
		.attr("stroke-width", 2)
		.attr("d", path_string)
		// tooltip event
		.on("mousemove", function() {mouseover(tooltip, lolli_data, d3.event)})
		.on("mouseout", function() {mouseout(tooltip)});
	
	var group = d3.select('#peakflow_bar svg .group');
	group.append("circle")
		.attr('class', 'cir')
		.attr('r', "4.5")
		.attr('cx', lolli_pos_x)
		.attr('cy', lolli_pos_y)
		.on("mousemove", function() {mouseover(tooltip, lolli_data, d3.event)})
		.on("mouseout", function() {mouseout(tooltip)});

	function mouseover(tooltip, d, event) {
		tooltip.transition().duration(500).style("opacity", .9);
		tooltip.style("display", "inline-block")
			.style("left", (event.pageX) + 10 + "px")
			.style("top", (event.pageY - 70) + "px")
			.html((d.label) + "<br>" + (d.value) + " cfs");
	}
	function mouseout(tooltip) {tooltip.style("display", "none");}
});