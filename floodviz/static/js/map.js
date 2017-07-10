document.addEventListener("DOMContentLoaded", function (event) {
	"use strict";

	// Define helper functions
	function degreesToRadians(degrees) {
		return degrees * Math.PI / 180;
	}

	function radiansToDegrees(radians) {
		return radians * 180 / Math.PI;
	}

	// read in projection information
	var proj = proj4(FV.mapinfo.proj4string);

	var project = function (lambda, phi) {
		return proj.forward([lambda, phi].map(radiansToDegrees));
	};

	project.invert = function (x, y) {
		return proj.inverse([x, y]).map(degreesToRadians);
	};

	//Define map projection
	var projection = d3.geoProjection(project);

	// Give projection initial rotation and scale
	projection
		.scale(1)
		.translate([0, 0]);

	//Define path generator
	var path = d3.geoPath().projection(projection);

	var height = FV.mapinfo.height;
	var width = FV.mapinfo.width;

	// Tooltip
	var maptip = d3.select("body")
		.append("div")
		.attr("class", "maptip");

	//Create SVG element
	var svg = d3.select("#map")
		.append("svg")
		.attr("width", width)
		.attr("height", height);


	// set bounding box to values provided
	var b = path.bounds(FV.mapinfo.bounds);


	var s = FV.mapinfo.scale / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height);
	var t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

	// Update the projection
	projection
		.scale(s)
		.translate(t);


	// add layers in sensible order
	add_paths(FV.mapinfo.bg_data, "background");
	add_paths(FV.mapinfo.rivers_data, "river");
	add_circles(FV.mapinfo.ref_data, "ref-point", 2);
	var sites = add_circles(FV.mapinfo.site_data, "gage-point", 3);
	sites.selectAll("circle")
		.on('mousemove', function (d) {
			maptip.transition().duration(500);
			maptip.style("display", "inline-block")
				.style("left", (d3.event.pageX) + 10 + "px")
				.style("top", (d3.event.pageY - 70) + "px")
				.html((d.properties.name));
		})
		.on("mouseout", function (d) { maptip.style("display", "none");});


	if (FV.mapinfo.debug) {
		add_circles(FV.mapinfo.bounds, "debug-point", 3)
	}
	/**
	 * Add circles to the map.
	 * @param data The geojson to be added to the svg
	 * @param classname The class to be given to each element for use in CSS
	 * @param radius The radius of each circle. This cannot be set from CSS
	 */
	function add_circles(data, classname, radius) {
		var group = svg.append("g");
		group.selectAll("circle")
			.data(data.features)
			.enter()
			.append("circle")
			.attr("r", radius)
			.attr("transform", function (d) {
				return "translate(" + projection(d.geometry.coordinates) + ")";
			})
			.attr("class", function(d) {
				if (classname === 'gage-point') {
					classname += ' ' + d.properties.id;
				}
			})
			.attr("class", classname)
		return (group);
	}

	/**
	 * Add paths to the map
	 * @param data The geojson to be added to the svg
	 * @param classname The class to be given to each element for use in CSS
	 */
	function add_paths(data, classname) {
		var group = svg.append("g");
		group.selectAll("path")
			.data(data.features)
			.enter()
			.append("path")
			.attr("d", path)
			.attr("class", classname);
	}
});