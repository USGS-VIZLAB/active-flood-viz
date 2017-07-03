// document.addEventListener("DOMContentLoaded", function(event) {
//
// 	"use strict";
//
// 	// Collect and set hydrograph aspect ratio data
// 	var hydrograph = document.getElementById('hydrograph');
// 	hydrograph.style.height = FV.hydrometa['height'];
// 	hydrograph.style.width = FV.hydrometa['width'];

// D3 data import
// d3.json('../static/data/hydrograph_data.json', function(data) {
//
// 	nv.addGraph( function() {
//
// 		var getX = function(d) { return d.time_mili };
// 		var getY = function(d) { return d.value };
//
// 		// might want to switch to lineChart(). When cumulative line chart is clicked, the Y axis freaks out and reverts back to issue at https://github.com/novus/nvd3/issues/695 #
// 		var chart = nv.models.cumulativeLineChart()
// 				.x( getX )  // this value is stored in milliseconds since epoch (converted in data_format.py with datetime)
// 				.y( getY )
// 				.color(["#0000FF"])
// 				.useVoronoi(true)
// 				.clipVoronoi(false)
// 				.useInteractiveGuideline(false)
// 				.yScale(d3.scale.log())	// Logarithmic Y axis. (GM - I think this make the flood event less decipherable in the visual but it probably scales better)
// 				.margin({left: 120, top: 60})
// 				.showLegend(false)
// 				.showControls(false);
//
// 		chart.xAxis.axisLabel(" Date (M-D-Y H:M:S)")
// 				.axisLabelDistance(10)
// 				.ticks(5)
// 				.tickFormat(function(d){return d3.time.format('%m-%d-%y %H:%M:%S %Z')(new Date(d))});
//
// 		chart.yAxis.axisLabel('Discharge (cubic feet per second)')
// 				.axisLabelDistance(40)
// 				//.ticks(5)
// 				.tickValues([10, 100, 1000, 10000, 100000])
// 				.tickFormat(function(d) { return d3.format(",")(d) + " cfps"});
//
// 		d3.select('#hydrograph svg').datum(data).call(chart);
//
// 		nv.utils.windowResize(chart.update);
// 		return chart;
//
// 	});
//
// });

// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 600 - margin.left - margin.right,
    height = 270 - margin.top - margin.bottom;

// Parse the date / time
var parseDate = d3.timeParse("%m-%d");

// Set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

// Define the line
var valueline = d3.line()
    .x(function(d) { return x(d.time_mili); })
    .y(function(d) { return y(d.value); });

// Adds the svg canvas
var svg = d3.select("#hydrograph")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

// Get the data
d3.json("../static/data/hydrograph_data.json", function(error, data) {
    data.forEach(function(d) {
		d.time_mili = d.time_mili;
		d.value = +d.value;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.time_mili; }));
    y.domain([0, d3.max(data, function(d) { return d.value; })]);

    // Nest the entries by site number
    var dataNest = d3.nest()
        .key(function(d) {return d.key;})
        .entries(data);

    // Loop through each symbol / key
    dataNest.forEach(function(d) {

        svg.append("path")
            .attr("class", "line")
            .attr("id", d.key)
            .attr("d", valueline(d.values));

    });

    // Add the X Axis
    svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add the Y Axis
    svg.append("g")
      .attr("class", "axis")
      .call(d3.axisLeft(y));

});


