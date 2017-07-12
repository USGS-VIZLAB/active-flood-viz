"use strict";

FV.hydromodule = function (options) {

	var self = {};

	self.display_ids = options.display_ids;
	var subset_data = function(data){
		var toKeep = [];
		data.forEach(function(d){
			if(self.display_ids.indexOf(d.key) !== -1) {
				toKeep.push(d);
			}
		});
		return toKeep;
	};

	var margin = {top: 30, right: 20, bottom: 30, left: 50};

	var height = options.height - margin.top - margin.bottom;
	var width = options.width - margin.left - margin.right;
	var sel_div = options.div_id;
	// Adds the svg canvas
	var svg = null;
	// Focus for hydrograph hover tooltip
	var focus = null;
	// Voronoi layer
	var voronoi_group = null;
	// Define the voronoi
	var voronoi = d3.voronoi()
		.x(function (d) {
			return x(d.time_mili);
		})
		.y(function (d) {
			return y(d.value);
		})
		.extent([[-margin.left, -margin.top], [width + margin.right, height + margin.bottom]])
	// Define the line
	var line = d3.line()
		.x(function (d) {
			return x(d.time_mili);
		})
		.y(function (d) {
			return y(d.value);
		});
	// Set the ranges
	var x = d3.scaleTime().range([0, width]);
	var y = d3.scaleLog().range([height, 0]);

	/**
	 * Updates the SVG figure.
	 * @param List of data objects
	 */
	var update = function(data) {
		// recreate svg
		svg = d3.select(sel_div)
				.append("svg")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform",
					"translate(" + margin.left + "," + margin.top + ")");

		data.forEach(function (d) {
				d.value = Number(d.value);
		});
		// Scale the range of the data
		x.domain(d3.extent(data, function (d) {
			return d.time_mili;
		}));
		y.domain([20, d3.max(data, function (d) {
			return d.value;
		})]);
		// Nest the entries by site number
		var dataNest = d3.nest()
			.key(function (d) {
				return d.key;
			})
			.entries(data);
		// Loop through each symbol / key
		dataNest.forEach(function (d) {
			var map_site = document.getElementById('map' + d.key);
			map_site.classList.add('accent');
			svg.append("g")
				.attr('class', 'hydro-inactive')
				.append("path")
				.attr("id", "hydro" + d.key)
				.attr("d", line(d.values));
		});
		// Add the X Axis
		svg.append("g")
			.attr("class", "axis")
			.attr("transform", "translate(0," + height + ")")
			.call(d3.axisBottom(x).tickFormat(d3.timeFormat("%B %e")));

		// Add the Y Axis
		svg.append("g")
			.attr("class", "axis")
			.call(d3.axisLeft(y).ticks(10, ".0f"));

		// Tooltip
		focus = svg.append("g")
				.attr("transform", "translate(-100,-100)")
				.attr("class", "focus");

		focus.append("circle")
				.attr("r", 3.5);

		focus.append("text")
				.attr("y", -10);

		// Voronoi Layer
		voronoi_group = svg.append("g")
				.attr("class", "voronoi");
		voronoi_group.selectAll("path")
				.data(voronoi.polygons(d3.merge(dataNest.map(function (d) {
					return d.values
				}))))
				.enter().append("path")
				.attr("d", function (d) {
					return d ? "M" + d.join("L") + "Z" : null;
				})
				.on("mouseover", self.mouseover)
				.on("mouseout", self.mouseout)
				.on("click", function(d) {return self.click(d, data)})
	};

	self.init = function() {
		var data_path = options.data_path;
		// Get the data
		d3.json(data_path, function (error, data) {
			if(error){ console.error(error); }
			data = subset_data(data);
			update(data);
		});
	};

	self.mouseover = function(d) {
		d3.select("#hydro" + d.data.key).attr("class", "hydro-active");
		focus.attr("transform", "translate(" + x(d.data.time_mili) + "," + y(d.data.value) + ")");
		focus.select("text").html(d.data.key + ": " + d.data.value + " cfs " + " " + d.data.time + " " + d.data.timezone);
		// Interative linking with map
		FV.map_figure.mousemove(d.data.name, d.data.key);
	};

	self.mouseout = function(d) {
		d3.select("#hydro" + d.data.key).attr("class", "hydro-inactive");
		focus.attr("transform", "translate(-100,-100)");
		// Interative linking with map
		FV.map_figure.mouseout();
	};

	self.click = function(d, data) {
		d3.select("svg").remove();
			var new_data = [];
			var i;
			for (i=0; i<data.length; i++) {
				if (data[i]["key"] !== d.data.key) {
					new_data.push(data[i]);
				}
			}
			update(new_data);
		// Interative linking with map
		FV.map_figure.removeaccent(d.data.key);
	};

	return self

};

