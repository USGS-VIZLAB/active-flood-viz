
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
	var make_lines_bland = function (exemptkey){
		if(options.display_ids.indexOf(exemptkey) !== -1) {
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
			.attr('transform',
				'translate(' + margin.left + ',' + margin.top + ')');

		// Watermark
		var watermark = svg.append('g')
			.attr('id', 'usgs-watermark')
			.attr('transform', 'translate(' + 1/5 * width + ',' +1/4 * height +')scale(0.50)');
		watermark.append('path')
			.attr('d', 'm234.95 15.44v85.037c0 17.938-10.132 36.871-40.691 36.871-27.569 0-40.859-14.281-40.859-' +
				'36.871v-85.04h25.08v83.377c0 14.783 6.311 20.593 15.447 20.593 10.959 0 15.943-7.307 15.943-' +
				'20.593v-83.377h25.08m40.79 121.91c-31.058 0-36.871-18.27-35.542-39.03h25.078c0 11.462 0.5 ' +
				'21.092 14.282 21.092 8.472 0 12.62-5.482 12.62-13.618 0-21.592-50.486-22.922-50.486-58.631 ' +
				'0-18.769 8.968-33.715 39.525-33.715 24.42 0 36.543 10.963 34.883 36.043h-24.419c0-8.974-' +
				'1.492-18.106-11.627-18.106-8.136 0-12.953 4.486-12.953 12.787 0 22.757 50.493 20.763 50.493' +
				' 58.465 0 31.06-22.75 34.72-41.85 34.72m168.6 0c-31.06 0-36.871-18.27-35.539-39.03h25.075c0 ' +
				'11.462 0.502 21.092 14.285 21.092 8.475 0 12.625-5.482 12.625-13.618 0-21.592-50.494-' +
				'22.922-50.494-58.631 0-18.769 8.969-33.715 39.531-33.715 24.412 0 36.536 10.963 34.875 36.043h-' +
				'24.412c0-8.974-1.494-18.106-11.625-18.106-8.144 0-12.955 4.486-12.955 12.787 0 22.757 50.486 ' +
				'20.763 50.486 58.465 0 31.06-22.75 34.72-41.85 34.72m-79.89-46.684h14.76v26.461l-1.229 0.454c-3.816 ' +
				'1.332-8.301 2.327-12.453 2.327-14.287 0-17.943-6.645-17.943-44.177 0-23.256 0-44.348 15.615-44.348 ' +
				'12.146 0 14.711 8.198 14.933 18.107h24.981c0.198-23.271-14.789-36.043-38.42-36.043-41.021 0-42.52 ' +
				'30.724-42.52 60.954 0 45.507 4.938 63.167 47.12 63.167 9.784 0 25.36-2.211 ' +
				'32.554-4.18 0.436-0.115 1.212-0.596 1.212-1.216v-59.598h-38.612v18.09')
			.attr('class', 'watermark');
		watermark.append('path')
			.attr('d', 'm48.736 55.595l0.419 0.403c11.752 9.844 24.431 8.886 34.092 2.464 6.088-4.049 ' +
				'33.633-22.367 49.202-32.718v-10.344h-116.03v27.309c7.071-1.224 18.47-0.022 32.316 12.886m43.651 ' +
				'45.425l-13.705-13.142c-1.926-1.753-3.571-3.04-3.927-3.313-11.204-7.867-21.646-5.476-' +
				'26.149-3.802-1.362 0.544-2.665 1.287-3.586 1.869l-28.602 19.13v34.666h116.03v-24.95c-2.55 ' +
				'1.62-18.27 10.12-40.063-10.46m-44.677-42.322c-0.619-0.578-1.304-1.194-1.915-1.698-13.702-10.6-' +
				'26.646-5.409-29.376-4.116v11.931l6.714-4.523s10.346-7.674 26.446 0.195l-1.869-1.789m16.028 ' +
				'15.409c-0.603-0.534-1.214-1.083-1.823-1.664-12.157-10.285-23.908-7.67-28.781-5.864-1.382 ' +
				'0.554-2.7 1.303-3.629 1.887l-13.086 8.754v12.288l21.888-14.748s10.228-7.589 26.166 ' +
				'0.054l-0.735-0.707m68.722 12.865c-4.563 3.078-9.203 6.203-11.048 7.441-4.128 2.765-13.678 ' +
				'9.614-29.577 2.015l1.869 1.797c0.699 0.63 1.554 1.362 2.481 2.077 11.418 8.53 23.62 ' +
				'7.303 32.769 1.243 1.267-0.838 2.424-1.609 3.507-2.334v-12.234m0-24.61c-10.02 6.738-23.546 ' +
				'15.833-26.085 17.536-4.127 2.765-13.82 9.708-29.379 2.273l1.804 1.729c0.205 0.19 0.409 0.375 ' +
				'0.612 0.571l-0.01 0.01 0.01-0.01c12.079 10.22 25.379 8.657 34.501 2.563 5.146-3.436 12.461-8.38 ' +
				'18.548-12.507l-0.01-12.165m0-24.481c-14.452 9.682-38.162 25.568-41.031 27.493-4.162 2.789-13.974 ' +
				'9.836-29.335 2.5l1.864 1.796c1.111 1.004 2.605 2.259 4.192 3.295 10.632 6.792 21.759 5.591 ' +
				'30.817-0.455 6.512-4.351 22.528-14.998 33.493-22.285v-12.344')
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
		options.display_ids.forEach(function(id) {
			d3.select('#hydro' + id).attr('class', 'hydro-inactive');
		})

	};

	return self
}
