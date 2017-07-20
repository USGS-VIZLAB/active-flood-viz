(function () {
	"use strict";
	/**
	 * @param {Object} options - holds options for the configuration of the hydrograph
	 *    Non-optional Keys include:
	 *        'height' v(int) - height of the graph
	 *        'width' v(int) - width of the graph
	 *        'data' v(list) - A list of objects representing data points
	 *        'div_id' v(string) - id for the container for this graph
	 *    Optional Keys include:
	 *        'hover_in' - linked function for hover_in.
	 *        'hover_out' - linked function for hover_out.
	 *        'click_on' - linked function for clicking on hydrograph to accent mapsite.
	 *        'click_off' - linked function for clicking hydrograph to unaccent mapsite.
	 *
	 * hydromodule is a module for creating hydrographs using d3. Pass it a javascript object
	 * specifying config options for the graph. Call init() to create the graph. Other public functions
	 * handle user events and link to other modules.
	 *
	 *
	 */
	FV.hydromodule = function (options) {

		var self = {};

		var margin = {top: 60, right: 20, bottom: 30, left: 50};
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
		 * @returns {Array} The entries of the original `data` whose `key` values are elements of display_ids.
		 */
		var subset_data = function (full_data) {
			var toKeep = [];
			full_data.forEach(function (d) {
				if (FV.hydrograph_display_ids.indexOf(d.key) !== -1) {
					toKeep.push(d);
				}
			});
			return toKeep;
		};

		/**
		 *
		 * Draws the svg, scales the range of the data, and draws the line for each site
		 * all based on the data set as it was passed in. Called as needed
		 * when data changes (as in removal of a line).
		 *
		 */
		var update = function () {

				// Cut the data down to sites we want to display
				var sub_data = subset_data(options.data);
				// Remove the current version of the graph if one exists
				var current_svg = d3.select(options.div_id + " svg");
				if (current_svg) {
					current_svg.remove();
				}
				// recreate svg
				svg = d3.select(options.div_id)
					.append("svg")
					.attr("width", width + margin.left + margin.right)
					.attr("height", height + margin.top + margin.bottom)
					.append("g")
					.attr("transform",
						"translate(" + margin.left + "," + margin.top + ")");

				var graph_data = sub_data.map(function (d) {
					return {
						"date": d.date,
						"key": d.key,
						"name": d.name,
						"time": d.time,
						"time_mili": d.time_mili,
						"timezone": d.timezone,
						"value": Number(d.value)
					};

				});

				// Scale the range of the data
				x.domain(d3.extent(graph_data, function (d) {
					return d.time_mili;
				}));
				y.domain([d3.min(graph_data, function (d) {
					return d.value;
				}), d3.max(graph_data, function (d) {
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
					.on("mouseover", function (d) {
						options.hover_in(d.data.name, d.data.key);
						self.activate_line(d.data.key);
						self.series_tooltip_show(d);
					})
					.on("mouseout", function (d) {
						options.hover_out();
						self.deactivate_line(d.data.key);
						self.series_tooltip_remove(d.data.key);
					})
					.on("click", function (d) {
						options.click_off(d.data.key);
						self.remove_series(d.data.key);
					});

		};

		/**
		 * Initialize the Hydrograph
		 */
		self.init = function (linked_interactions) {
			update(linked_interactions);
		};
		/**
		 * Displays tooltip for hydrograph at a data point in addition to
		 * corresponding map site tooltip.
		 */
		self.series_tooltip_show = function (d) {
			focus.attr("transform", "translate(" + x(d.data.time_mili) + "," + y(d.data.value) + ")");
			focus.select("text").html(d.data.key + ": " + d.data.value + " cfs " + " " + d.data.time + " " + d.data.timezone);
		};

		/**
		 * Removes tooltip view from the hydrograph series
		 * as well as the correspond mapsite tooltip.
		 */
		self.series_tooltip_remove = function (sitekey) {
			focus.attr("transform", "translate(-100,-100)");
		};

		/**
		 * Removes a line from the hydrograph. This resizes data
		 * appropriately and removes accents from the corresponding
		 * site on the map.
		 */
		self.remove_series = function (sitekey, linked_interactions) {
			var keep_ids = FV.hydrograph_display_ids;
			keep_ids.splice(FV.hydrograph_display_ids.indexOf(sitekey), 1);
			self.change_lines(keep_ids, linked_interactions);
			options.hover_out();
		};
		/**
		 * Update the value of display_ids and call update to redraw the graph to match.
		 * @param new_display_ids The new set of gages to be displayed.
		 */
		self.change_lines = function (new_display_ids, linked_interactions) {
			FV.hydrograph_display_ids = new_display_ids;
			update(linked_interactions);
		};
		/**
		 * Highlight a line.
		 * @param sitekey the site number of the line to be highlighted
		 */
		self.activate_line = function (sitekey) {
			d3.select('#hydro' + sitekey).attr('class', 'hydro-active');
		};
		/**
		 * Un-highlight a line
		 * @param sitekey the site number of the line to be un-highlighted
		 */
		self.deactivate_line = function (sitekey) {
			d3.select('#hydro' + sitekey).attr('class', 'hydro-inactive');
		};
		return self
	};
}());
