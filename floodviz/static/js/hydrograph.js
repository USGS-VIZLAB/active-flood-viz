(function () {
	"use strict";
	/**
		* @param {Javascript Object} options - holds options for the configuration of the hydrograph
		*	All keys are not optional.
		*  Keys include: 	
		* 					'height' v(int) - height of the graph 
		*					'width' v(int) - width of the graph
		*					'data_path' v(string) - path to the data file for this graph
		*					'div_id' v(string) - id for the container for this graph
		*
		* hydromodule is a module for creating hydrographs using d3. Pass it a javascript object 
		* specifying config options for the graph. Call init() to create the graph. Other pulic fuctions
		* handle user events and link to other modules. 
		* 
		*
	*/
	FV.hydromodule = function (options) {

		var self = {};
		var margin = {top: 30, right: 20, bottom: 30, left: 50};

		var height = options.height - margin.top - margin.bottom;
		var width = options.width - margin.left - margin.right;
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
			* @param {Array} data -- an array containing the json data to be drawn
			*
			* Draws the svg, scales the range of the data, and draws the line for each site
			* all based on the data set as it was passed in. Called as needed
			* when data changes (as in removal of a line).
			*
		*/
		var update = function(data) {
			// recreate svg
			svg = d3.select(options.div_id)
					.append("svg")
					.attr("width", width + margin.left + margin.right)
					.attr("height", height + margin.top + margin.bottom)
					.append("g")
					.attr("transform",
						"translate(" + margin.left + "," + margin.top + ")");
			
			var graph_data = data.map(function(d) {
				return  { "date": d.date,
				"key": d.key, 
				"name": d.name, 
				"time": d.time, 
				"time_mili": d.time_mili,
				"timezone": d.timezone,
				"value": Number(d.value) };
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
				.entries(graph_data);
			// Loop through each symbol / key
			dataNest.forEach(function (d) {
				var map_site = document.getElementById('map' + d.key);
				map_site.classList.add('accent');
				svg.append("g")
					.attr('class', 'gages')
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
					.on("click", function(d) {return self.click(d.data.key, graph_data)})
		};
		/**
		 * Initalize the Hydrograph
		 */
		self.init = function() {
			var data_path = options.data_path;
			// Get the data
			d3.json(data_path, function (error, data) {
				update(data);
			});
		};
		/**
		 * Handle all mouse over movements for calling element. 
		 */
		self.mouseover = function(d) {
			d3.select(d.data.name).classed("gage--hover", true);
			focus.attr("transform", "translate(" + x(d.data.time_mili) + "," + y(d.data.value) + ")");
			focus.select("text").html(d.data.key + ": " + d.data.value + " cfs " + " " + d.data.time + " " + d.data.timezone);
			// Interative linking with map
			FV.map_figure.mousemove(d.data.name, d.data.key);
		};
		/**
		 * Handle all mouse out movements for calling element. 
		 */
		self.mouseout = function(d) {
			d3.select(d.data.name).classed("gage--hover", false);
			focus.attr("transform", "translate(-100,-100)");
			// Interative linking with map
			FV.map_figure.mouseout();
		};
		/**
		 * Handle all click events for calling element. 
		 */
		self.click = function(key, data) {
			d3.select("svg").remove();
			var new_data = data.filter(function(d) {
				return d.key !== key;
			});
			update(new_data);
			// Interative linking with map
			FV.map_figure.removeaccent(key);
		};

		return self

	};

}());

