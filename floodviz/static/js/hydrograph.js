'use strict';
/**
 * @param {Object} options - holds options for the configuration of the hydrograph
 *    Non-optional Keys include:
 *        @prop 'height' v(int) - height of the graph
 *        @prop 'width' v(int) - width of the graph
 *        @prop 'div_id' v(string) - id for the container for this graph
 *        @prop 'display_ids' v(list) - default series to show on hydrograph
 *
 * hydromodule is a module for creating hydrographs using d3. Pass it a javascript object
 * specifying config options for the graph. Call init() to create the graph. Linked
 * interaction functions for other figures should be passed to init in and object.
 *
 */
var hydromodule = function (options) {
	var self = {};
	var data_global = null;

	var state = {};

	var default_display_ids = null;
	var timer = null;
	var dblclick_armed = false;

	var margin = {top: 60, right: 0, bottom: 30, left: 40};
	var width = 500 - margin.left - margin.right;
	var height = 500 * (options.height / options.width) - margin.top - margin.bottom;

	// Adds the svg canvas
	var svg = null;
	// for hydrograph hover tooltip
	var hydrotip = null;
	// Voronoi layer
	var voronoi_group = null;
	// Define the voronoi
	var voronoi = d3.voronoi()
		.x(function (d) {
			return scaleX(d.time_mili);
		})
		.y(function (d) {
			return scaleY(d.value);
		})
		.extent([[-margin.left, -margin.top], [width + margin.right, height + margin.bottom]]);
	// Define the line
	var line = d3.line()
		.x(function (d) {
			return scaleX(d.time_mili);
		})
		.y(function (d) {
			return scaleY(d.value);
		});
	// Set the ranges
	var scaleX = d3.scaleTime().range([0, width]);
	var scaleY = d3.scaleLog().range([height, 0]);

	// Google Analytics Boolean Trackers
	var hydro_moused_over = false;

	/**
	 * Filters a set of data based on the ids listed in display_ids
	 * @returns {Array} The entries of the original `data` whose `key` values are elements of display_ids.
	 */
	var subset_data = function (full_data) {
		var toKeep = [];
		full_data.forEach(function (d) {
			if (options.display_ids.indexOf(d.key) !== -1) {
				toKeep.push(d);
			}
		});
		return toKeep;
	};

	/**
	 * De-emphasize all but one specified line
	 * @param exemptkey - The key of the one line that should not be de-emphasized
	 */
	var make_lines_bland = function (exemptkey) {
		if (options.display_ids.indexOf(exemptkey) !== -1) {
			options.display_ids.forEach(function (id) {
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
		options.display_ids.forEach(function (id) {
			if (default_display_ids.indexOf(id) === -1) {
				self.linked_interactions.click(id);
			}
		});
		default_display_ids.forEach(function (id) {
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
		var sub_data = subset_data(data_global);
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
			.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

		// Save the locations of the edges of the visible svg
		state.edges = {
			'l': - (margin.left + margin.right),
			'r': width + margin.right,
			't': -(margin.top + margin.bottom)
		};

		// Watermark
		var watermark = svg.append('g')
			.attr('id', 'usgs-watermark')
			.attr('transform', 'translate(' + 1/4 * width + ',' +1/4 * height +')scale(0.45)'); // watermark position
		watermark.append('path')
			.attr('d', options.watermark_path_1)
			.attr('class', 'watermark');
		watermark.append('path')
			.attr('d', options.watermark_path_2)
			.attr('class', 'watermark');

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
		scaleX.domain(d3.extent(graph_data, function (d) {
			return d.time_mili;
		}));
		scaleY.domain([d3.min(graph_data, function (d) {
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
			.call(d3.axisBottom(scaleX).tickFormat(d3.timeFormat('%B %e')));

		// Add the Y Axis
		svg.append('g')
			.attr('class', 'axis')
			.call(d3.axisLeft(scaleY).ticks(10, '.0f'));

		// Tooltip
		hydrotip = svg.append('g')
			.attr('class', 'hydrotip-hide');
		hydrotip.append('rect');
		hydrotip.append('circle')
			.attr('r', 3.5);
		hydrotip.append('text')
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
				// Only log first hover of hydrograph per session
				if (!hydro_moused_over) {
					FV.ga_send_event('Hydrograph', 'hover_series', d.data.key);
					hydro_moused_over = true;
				}
			})
			.on('mouseout', function (d) {
				self.linked_interactions.hover_out();
				self.deactivate_line(d.data.key);
				self.series_tooltip_remove(d.data.key);
			})
			.on('click', function (d) {
				console.log(d3.mouse(this));
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
					FV.ga_send_event('Hydrograph', 'series_click_off', d.data.key);
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
	 *@param {array} data - times series data for the hydrograph. Each element is an object representing a data point.
	 *
	 *
	 */
	self.init = function (linked_interactions, data) {
		data_global = data;
		// use array.slice() to deep copy
		default_display_ids = options.display_ids.slice();
		self.linked_interactions = linked_interactions;
		update();
	};
	/**
	 * Returns the svg element node. Primarily used for thumb-nailing.
	 */
	self.get_svg_elem = function () {
		return d3.select(options.div_id);
	};
	/**
	 * Displays tooltip for hydrograph at a data point in addition to
	 * corresponding map site tooltip.
	 */
	self.series_tooltip_show = function (d) {
		const padding = 3;
		const scaled = {
			x: scaleX(d.data.time_mili),
			y: scaleY(d.data.value)
		};

		hydrotip.attr('transform', 'translate(' + scaleX(d.data.time_mili) + ',' + scaleY(d.data.value) + ')')
			.attr('class', 'hydrotip-show');
		const tiptext = hydrotip.select('text');
		tiptext.html(d.data.key + ': ' + d.data.value + ' cfs ' + ' ' + d.data.time + ' ' + d.data.timezone);
		const textbg = hydrotip.select('rect');
		const bound = tiptext._groups[0][0].getBBox();

		// Find the edges of the tooltip (left, right, and top)
		const tipedges = {
			'l': scaled.x - bound.width / 2,
			'r': scaled.x + bound.width / 2,
			't': scaled.y - bound.height
		};

		// store how much the tooltip has to be adjusted by to stay entirely visible
		var adjust = {
			'l': 0,
			'r': 0,
			't': 0
		};

		if(tipedges.l < state.edges.l){
			// this will be positive so it will be a shift to the right
			adjust.l = state.edges.l - tipedges.l
		}
		else if(tipedges.r > state.edges.r){
			// this will be negative, so a shift to the left
			adjust.r = state.edges.r - tipedges.r
		}
		if(tipedges.t < state.edges.t){
			// I haven't had this happen yet, so I'm leaving it for later.
			console.log('top');
		}

		tiptext.attr('transform', 'translate(' + (adjust.l + adjust.r) + ', 0)' );
		// One of adjust.l or adjust.r should always be 0.
		textbg.attr('x', bound.x - padding + adjust.l + adjust.r)
			.attr('y', bound.y - padding)
			.attr('width', bound.width + padding * 2)
			.attr('height', bound.height + padding * 2);
	};

	/**
	 * Removes tooltip view from the hydrograph series
	 * as well as the correspond mapsite tooltip.
	 */
	self.series_tooltip_remove = function () {
		hydrotip.attr('class', 'hydrotip-hide');
	};

	/**
	 * Removes a line from the hydrograph. This resizes data
	 * appropriately and removes accents from the corresponding
	 * site on the map.
	 */
	self.remove_series = function (sitekey) {
		var keep_ids = options.display_ids;
		keep_ids.splice(options.display_ids.indexOf(sitekey), 1);
		self.change_lines(keep_ids);
	};
	/**
	 * Update the value of display_ids and call update to redraw the graph to match.
	 * @param new_display_ids The new set of gages to be displayed.
	 */
	self.change_lines = function (new_display_ids) {
		options.display_ids = new_display_ids;
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
		options.display_ids.forEach(function (id) {
			d3.select('#hydro' + id).attr('class', 'hydro-inactive');
		})

	};

	return self
};
