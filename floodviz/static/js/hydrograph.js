"use strict";

FV.hydromodule = function (options) {

	var self = {};
	/**
	 * options.display_ids is the intiial value of display_ids and defines the set of sites to be displayed by default.
	 * display_ids is also used to keep track of the set of gages being displayed as this is changed by the user.
	 * This should be set ONLY via the change_lines function.
	 */
	var display_ids = options.display_ids;

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
		.extent([[-margin.left, -margin.top], [width + margin.right, height + margin.bottom]]);
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
	 * Filters a set of data based on the ids listed in display_ids
	 * @param data The dataset to be filtered
	 * @returns {Array} The entries of the original `data` whose `key` values are elements of display_ids.
	 */
	var subset_data = function (data) {
		var toKeep = [];
		data.forEach(function (d) {
			if (display_ids.indexOf(d.key) !== -1) {
				toKeep.push(d);
			}
		});
		return toKeep;
	};

	/**
	 * Updates the SVG figure.
	 * @param data: list of data objects
	 */
	var update = function (data) {
		// Cut the data down to sites we want to display
		data = subset_data(data);
		// Remove the current version of the graph if one exists
		if (svg !== null){
			d3.select(sel_div).select('svg').remove();
		}
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
			FV.map_figure.addaccent(d.key);
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
			.on("click", function (d) {return self.click(d)})
	};

	self.init = function () {
		var data_path = options.data_path;
		// Get the data
		d3.json(data_path, function (error, data) {
			if (error) { console.error(error); }
			// Used to store the entire data set before any filtering. This is used to produce new data sets.
			self.full_data = data;
			update(data);
		});
	};

	self.mouseover = function (d) {
		self.activate_line(d.data.key);
		focus.attr("transform", "translate(" + x(d.data.time_mili) + "," + y(d.data.value) + ")");
		focus.select("text").html(d.data.key + ": " + d.data.value + " cfs " + " " + d.data.time + " " + d.data.timezone);
		// Interative linking with map
		FV.map_figure.mousemove(d.data.name, d.data.key);
	};

	self.mouseout = function (d) {
		self.deactivate_line(d.data.key);
		focus.attr("transform", "translate(-100,-100)");
		// Interative linking with map
		FV.map_figure.mouseout();
	};

	/**
	 * Process a click: remove the line from the graph and un-accent the gage on the map
	 * @param d
	 */
	self.click = function (d) {
		FV.map_figure.removeaccent(d.data.key);
		var keep_ids = display_ids;
			keep_ids.splice(display_ids.indexOf(d.data.key), 1);
		self.change_lines(keep_ids);
	};
	/**
	 * Returns display_ids
	 * @returns {*} display_ids
	 */
	self.get_display_ids = function(){
		return display_ids;
	};

	/**
	 * Update the value of display_ids and call update to redraw the graph to match.
	 * @param new_display_ids The new set of gages to be displayed.
	 */
	self.change_lines = function (new_display_ids) {
		display_ids = new_display_ids;
		var new_data = [];
		self.full_data.forEach(function (d) {
			if (display_ids.indexOf(d.key) !== -1) {
				new_data.push(d);
			}
		});
		update(new_data);
	};
	/**
	 * Highlight a line.
	 * @param sitekey the site number of the line to be highlighted
	 */
	self.activate_line = function(sitekey){
		d3.select('#hydro' + sitekey).attr('class', 'hydro-active');
	};
	/**
	 * Un-highlight a line
	 * @param sitekey the site number of the line to be un-highlighted
	 */
	self.deactivate_line = function(sitekey){
		d3.select('#hydro' + sitekey).attr('class', 'hydro-inactive');
	};
	return self

};

