"use strict";

// define module for map interactios
FV.mapmodule = function (options) {

	var self = {};
	var height = options.height;
	var width = options.width;
	var proj = options.proj;
	var sel_div = options.div_id;
	var project = function (lambda, phi) {
		return proj.forward([lambda, phi].map(radiansToDegrees));
	};
	project.invert = function (x, y) {
		return proj.inverse([x, y]).map(degreesToRadians);
	};
	//Define map projection
	var projection = d3.geoProjection(project);
	// Give projection initial rotation and scale
	projection.scale(1).translate([0, 0]);
	//Define path generator
	var path = d3.geoPath().projection(projection);
	//Create SVG element
	var svg = d3.select(sel_div)
		.append("svg")
		.attr("width", width)
		.attr("height", height);
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
	 * 							If null, or not provided, no id will be given.
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
			.attr("id", function(d) {
				if (property_for_id && d.properties[property_for_id]) {
					return 'map' + d.properties[property_for_id];
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

	self.init = function() {

		var bounds = options.bounds;
		var scale = options.scale;
		var bg_data = options.bg_data;
		var rivers_data = options.rivers_data;
		var ref_data = options.ref_data;
		var site_data = options.site_data;

		// set bounding box to values provided
		var b = path.bounds(bounds);
		var s = scale / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height);
		var t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];
		// Update the projection
		projection.scale(s).translate(t);
		// Add layers
		add_paths(bg_data, "background");
		add_paths(rivers_data, "river");
		add_circles(ref_data, "ref-point", 2);
		// Add sites and bind events for site hovers
		var sites = add_circles(site_data, "gage-point", 3, 'id');
		sites.selectAll("circle")
			.on('mousemove', function(d) {return self.mousemove(d.properties.name, d.properties.id)})
			.on("mouseout", function(d) {return self.mouseout(d.properties.id)})
			.on('click', function(d) { return self.click(d.properties.id)});
		// Debug points
		if (FV.mapinfo.debug) {
			add_circles(FV.mapinfo.bounds, "debug-point", 3)
		}
	};

	self.mousemove = function (sitename, sitekey) {
		FV.hydro_figure.activate_line(sitekey);
		var gage_point_cords = document.getElementById('map'+sitekey).getBoundingClientRect();
		maptip.transition().duration(500);
		maptip.style("display", "inline-block")
			.style("left", (gage_point_cords.left) + 7 + "px")
			.style("top", (gage_point_cords.top - 30) + "px")
			.html((sitename));
	};
	self.mouseout = function (sitekey) {
		FV.hydro_figure.deactivate_line(sitekey);
		maptip.style("display", "none");
	};

	self.addaccent  = function(sitekey){
		d3.select('#map' + sitekey).attr('class', 'gage-point-accent');
	};

	self.removeaccent = function(sitekey) {
		d3.select('#map' + sitekey).attr('class', 'gage-point');
	};


	self.click = function(sitekey){
		var display_ids = FV.hydro_figure.get_display_ids();
		var being_displayed = display_ids.indexOf(sitekey) !== -1;
		if (being_displayed === true){
			self.removeaccent(sitekey);
			display_ids.splice(display_ids.indexOf(sitekey), 1)
		}
		else{
			self.addaccent(sitekey);
			display_ids.push(sitekey);
		}
		FV.hydro_figure.change_lines(display_ids);
		FV.hydro_figure.activate_line(sitekey);
	};

	return self
};


// Define helper functions
function degreesToRadians(degrees) {
	return degrees * Math.PI / 180;
}

function radiansToDegrees(radians) {
	return radians * 180 / Math.PI;
}


