(function() {
	"use strict";
	/**
	 * @param {Object} options - holds options for the configuration of the map.
	 * All keys are not optional.
	 * Keys include:
	 *    @prop 'height' v(int) - height of the map
	 *    @prop 'width' v(int) - width of the map
	 *    @prop 'proj' v(proj4) - map projection
	 *    @prop 'bounds' v(javascript object) - bounding box
	 *    @prop 'scale' v(int) - scale for map
	 *    @prop 'bg_data' v(javascript object) - background data
	 *    @prop 'rivers_data' v(geojson) - rivers data
	 *    @prop 'ref_data' v(javascript object) - reference data
	 *    @prop 'site_data' v(javascript object) - site data
	 *    @prop 'div_id' v(string) - id for the container for this graph
	 *
	 * mapmodule is a module for creating maps using d3. Pass it a javascript object
	 * specifying config options for the map. Call init() to create the map. Other pulic fuctions
	 * handle user events and link to other modules.
	 *
	 */
	FV.mapmodule = function (options) {

		var self = {};
		var project = function (lambda, phi) {
			return options.proj.forward([lambda, phi].map(radiansToDegrees));
		};
		project.invert = function (x, y) {
			return options.proj.inverse([x, y]).map(degreesToRadians);
		};
		//Define map projection
		var projection = d3.geoProjection(project);
		// Give projection initial rotation and scale
		projection.scale(1).translate([0, 0]);
		//Define path generator
		var path = d3.geoPath().projection(projection);
		//Create SVG element
		var svg = null;
		// Tooltip
		var maptip = d3.select("body")
			.append("div")
			.attr("id", "maptip");

		/**
		 * Add circles to the map.
		 * @param data The geojson to be added to the svg
		 * @param classname The class to be given to each element for use in CSS
		 * @param radius The radius of each circle. This cannot be set from CSS
		 * @param property_for_id The name of a field in the 'properties' of each feature, to be used for ID
		 *                            If null, or not provided, no id will be given.
		 */
		var add_circles = function (data, classname, radius, property_for_id) {
			var group = svg.append("g");
			group.selectAll("circle")
				.data(data.features)
				.enter()
				.append("circle")
				.attr("r", radius)
				.attr("transform", function (d) {
					return "translate(" + projection(d.geometry.coordinates) + ")";
				})
				.attr("id", function (d) {
					if (property_for_id && d.properties[property_for_id]) {
						return 'map' + d.properties[property_for_id];
					}
					else{
						return '';
					}
				})
				.attr("class", classname);
			return (group);
		};
		/**
		 * Add paths to the map
		 * @param data The geojson to be added to the svg
		 * @param classname The class to be given to each element for use in CSS
		 */
		var add_paths = function (data, classname) {
			var group = svg.append("g");
			group.selectAll("path")
				.data(data.features)
				.enter()
				.append("path")
				.attr("d", path)
				.attr("class", classname);
		};
		
		/**
		 * Initialize the Map
		 */
		self.init = function() {

			if (svg !== null) {
				d3.select(options.div_id).select('svg').remove();
			}
			svg = d3.select(options.div_id)
			.append("svg")
			.attr("width", options.width)
			.attr("height", options.height);
			
			// set bounding box to values provided
			var b = path.bounds(options.bounds);
			var s = options.scale / Math.max((b[1][0] - b[0][0]) / options.width, (b[1][1] - b[0][1]) / options.height);
			var t = [(options.width - s * (b[1][0] + b[0][0])) / 2, (options.height - s * (b[1][1] + b[0][1])) / 2];
			// Update the projection
			projection.scale(s).translate(t);
			// Add layers
			add_paths(options.bg_data, "background");
			add_paths(options.rivers_data, "river");
			add_circles(options.ref_data, "ref-point", 2);
			// Add sites and bind events for site hovers
			var sites = add_circles(options.site_data, "gage-point", 3, 'id');
			sites.selectAll("circle")
				.on('mousemove', function (d) {return self.site_tooltip_show(d.properties.name, d.properties.id)})
				.on("mouseout", function (d) {return self.site_tooltip_remove(d.properties.id)})
				.on('click', function (d) { return self.click(d.properties.id)});
			// Debug points
			if (FV.config.debug) {
				add_circles(options.bounds, "debug-point", 3)
			}
		};

		/**
		 * Shows sitename tooltip on map figure at correct location.
		 */
		self.site_tooltip_show = function (sitename, sitekey) {
			var gage_point_cords = document.getElementById('map'+sitekey).getBoundingClientRect();
			maptip.transition().duration(500);
			maptip.style("display", "inline-block")
				.style("left", (gage_point_cords.left) + 7 + "px")
				.style("top", (gage_point_cords.top - 30) + "px")
				.html((sitename));
		};
		/**
		 * Removes tooltip style from map site.
		 */
		self.site_tooltip_remove = function () {
			maptip.style("display", "none");
		};

		/**
		 * Remove/Add accent for a svg circle representing a site.
		 * Used by hydromodule for cross figure interactions.
		 */
		self.site_remove_accent = function (sitekey) {
			d3.select('#map' + sitekey).attr('class', 'gage-point');
		};
		self.site_add_accent = function (sitekey) {
			d3.select('#map' + sitekey).attr('class', 'gage-point-accent');
		};
		self.click = function (sitekey) {
			var new_display_ids = FV.hydrograph_display_ids;
			var being_displayed = new_display_ids.indexOf(sitekey) !== -1;
			if (being_displayed === true) {
				self.site_remove_accent(sitekey);
				new_display_ids.splice(new_display_ids.indexOf(sitekey), 1)
			}
			else {
				self.site_add_accent(sitekey);
				new_display_ids.push(sitekey);
			}
			options.change_lines(new_display_ids);
			options.activate_line(sitekey);
		};

		return self
	};

}());

// Define helper functions
function degreesToRadians(degrees) {
	"use strict";
	return degrees * Math.PI / 180;
}

function radiansToDegrees(radians) {
	"use strict";
	return radians * 180 / Math.PI;
}
