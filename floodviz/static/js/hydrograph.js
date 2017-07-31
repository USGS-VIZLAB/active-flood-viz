(function () {
	'use strict';
	/**
	 * @param {Object} options - holds options for the configuration of the hydrograph
	 *    Non-optional Keys include:
	 *        @prop 'height' v(int) - height of the graph
	 *        @prop 'width' v(int) - width of the graph
	 *        @prop 'data' v(list) - A list of objects representing data points
	 *        @prop 'div_id' v(string) - id for the container for this graph
	 *
	 * hydromodule is a module for creating hydrographs using d3. Pass it a javascript object
	 * specifying config options for the graph. Call init() to create the graph. Linked
	 * interaction functions for other figures should be passed to init in and object.
	 *
	 */
	FV.hydromodule = function (options) {

		var self = {};

		var default_display_ids = null;
		var timer = null;
		var dblclick_armed = false;

		var margin = {top: 60, right: 0, bottom: 30, left: 35};
		var height = 500 * (options.height / options.width) - margin.top - margin.bottom;
		var width = 500 - margin.left - margin.right;

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
		 * De-emphasize all but one specified line
		 * @param exemptkey - The key of the one line that should not be de-emphasized
		 */
		var make_lines_bland = function (exemptkey){
			if(FV.hydrograph_display_ids.indexOf(exemptkey) !== -1) {
				FV.hydrograph_display_ids.forEach(function (id) {
					if (id !== exemptkey) {
						d3.select('#hydro' + id).attr('class', 'hydro-inactive-bland');
					}
				})
			}
		};


		/**
		 * Show only the default set of lines on the hydrograph.
		 */
		var reset_hydrograph = function () {
			FV.hydrograph_display_ids.forEach(function (id) {
				if (default_display_ids.indexOf(id) === -1) {
					self.linked_interactions.click(id);
				}
			});
			default_display_ids.forEach(function(id){
				self.linked_interactions.accent_on_map(id);
			});
			// use array.slice() with no parameters to deep copy
			self.change_lines(default_display_ids.slice());
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
			var current_svg = d3.select(options.div_id + ' svg');
			if (current_svg) {
				current_svg.remove();
			}
			// recreate svg
			svg = d3.select(options.div_id)
				.append('svg')
				.attr("preserveAspectRatio", "xMinYMin meet")
				.attr("viewBox", "0 0 " + (width + margin.left + margin.right ) + " " + (height + margin.top + margin.bottom ))
				.append('g')
				.attr('transform',
					'translate(' + margin.left + ',' + margin.top + ')');

			var graph_data = sub_data.map(function (d) {
				return {
					'date': d.date,
					'key': d.key,
					'name': d.name,
					'time': d.time,
					'time_mili': d.time_mili,
					'timezone': d.timezone,
					'value': Number(d.value)
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
				svg.append('g')
					.attr('class', 'hydro-inactive')
					.append('path')
					.attr('id', 'hydro' + d.key)
					.attr('d', line(d.values));
			});
			// Make transparent background for lines
			svg.append('g')
				.attr('id', 'hydro-background')
				.append('rect')
				.attr('x', 0)
				.attr('y', 0)
				.attr('height', height)
				.attr('width', width)
				.on('dblclick', function () {
					reset_hydrograph();
				});

			// Add the X Axis
			svg.append('g')
				.attr('class', 'axis')
				.attr('transform', 'translate(0,' + height + ')')
				.call(d3.axisBottom(x).tickFormat(d3.timeFormat('%B %e')));

			// Add the Y Axis
			svg.append('g')
				.attr('class', 'axis')
				.call(d3.axisLeft(y).ticks(10, '.0f'));

			// Tooltip
			focus = svg.append('g')
				.attr('transform', 'translate(-100,-100)')
				.attr('class', 'focus');
			focus.append('circle')
				.attr('r', 3.5);

			focus.append('text')
				.attr('y', -10);

			// Voronoi Layer
			voronoi_group = svg.append('g')
				.attr('class', 'voronoi');
			voronoi_group.selectAll('path')
				.data(voronoi.polygons(d3.merge(dataNest.map(function (d) {
					return d.values
				}))))
				.enter().append('path')
				.attr('d', function (d) {
					return d ? 'M' + d.join('L') + 'Z' : null;
				})
				.on('mouseover', function (d) {
					self.linked_interactions.hover_in(d.data.name, d.data.key);
					self.activate_line(d.data.key);
					self.series_tooltip_show(d);
				})
				.on('mouseout', function (d) {
					self.linked_interactions.hover_out();
					self.deactivate_line(d.data.key);
					self.series_tooltip_remove(d.data.key);
				})
				.on('click', function (d) {
					if (dblclick_armed) {
						clearTimeout(timer);
						reset_hydrograph();
						dblclick_armed = false;
					}
					else {
						dblclick_armed = true;
						timer = setTimeout(function () {
							self.linked_interactions.click(d.data.key);
							self.linked_interactions.hover_out(d.data.key);
							self.remove_series(d.data.key);
							dblclick_armed = false;
						}, 200);
					}
				});

		};

		/**
		 * Initialize the Hydrograph.
		 *
		 *@param {Object} linked_interactions - Object holding functions that link to another figure's interactions.
		 *                                        Pass null if there are no such interactions to link.
		 *        @prop 'hover_in' - linked interaction function for hover_in events on this figure.
		 *        @prop 'hover_out' - linked interaction function for hover_out events on this figure.
		 *        @prop 'click' - linked interaction function for click events on this figure.
		 *
		 *
		 */
		self.init = function (linked_interactions) {
			// use array.slice() to deep copy
			default_display_ids = FV.hydrograph_display_ids.slice();
			self.linked_interactions = linked_interactions;
			update();
		};
		/**
		 * Displays tooltip for hydrograph at a data point in addition to
		 * corresponding map site tooltip.
		 */
		self.series_tooltip_show = function (d) {
			focus.attr('transform', 'translate(' + x(d.data.time_mili) + ',' + y(d.data.value) + ')');
			focus.select('text').html(d.data.key + ': ' + d.data.value + ' cfs ' + ' ' + d.data.time + ' ' + d.data.timezone);
		};

		/**
		 * Removes tooltip view from the hydrograph series
		 * as well as the correspond mapsite tooltip.
		 */
		self.series_tooltip_remove = function (sitekey) {
			focus.attr('transform', 'translate(-100,-100)');
		};

		/**
		 * Removes a line from the hydrograph. This resizes data
		 * appropriately and removes accents from the corresponding
		 * site on the map.
		 */
		self.remove_series = function (sitekey) {
			var keep_ids = FV.hydrograph_display_ids;
			keep_ids.splice(FV.hydrograph_display_ids.indexOf(sitekey), 1);
			self.change_lines(keep_ids);
		};
		/**
		 * Update the value of display_ids and call update to redraw the graph to match.
		 * @param new_display_ids The new set of gages to be displayed.
		 */
		self.change_lines = function (new_display_ids) {
			FV.hydrograph_display_ids = new_display_ids;
			update();
		};
		/**
		 * Highlight a line, de-emphasize all other lines
		 * @param sitekey the site number of the line to be highlighted
		 */
		self.activate_line = function (sitekey) {
			make_lines_bland(sitekey);
			d3.select('#hydro' + sitekey).attr('class', 'hydro-active');
		};
		/**
		 * Set all lines to inactive
		 */
		self.deactivate_line = function () {
			FV.hydrograph_display_ids.forEach(function(id) {
				d3.select('#hydro' + id).attr('class', 'hydro-inactive');
			})

		};
		return self
	};
}());
