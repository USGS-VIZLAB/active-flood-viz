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

    // Read in height and width
    var height = FV.mapinfo.height;
    var width = FV.mapinfo.width;

    //Create SVG element
    var svg = d3.select("#map")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // read in geojson for sites
    var site_data = FV.mapinfo.site_data;

    // set bounding box to values provided
    var b = path.bounds(FV.mapinfo.bounds);


    var s = FV.mapinfo.scale / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height);
    var t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

    // Update the projection
    projection
        .scale(s)
        .translate(t);

    // Define order in which layers should be added
    var bg = svg.append("g");
    var ref = svg.append("g");
    var sites = svg.append("g");
    
    // Tooltip
    var maptip = d3.select("body")
        .append("div")
        .attr("class", "maptip");


    // Bind data and create one path per GeoJSON feature
    // Add sites to the map
    sites.selectAll("circle")
        .data(site_data.features)
        .enter()
        .append("circle")
        .attr("r", 3)
        .attr("transform", function (d) {
            return "translate(" + projection(d.geometry.coordinates) + ")";
        })
        .attr("class", "gage-point")
        .on('mousemove', function(d) {
            maptip.transition().duration(500).style("opacity", .9);
            maptip.style("display", "inline-block")
            .style("left", (d3.event.pageX) + 10 + "px")
            .style("top", (d3.event.pageY - 70) + "px")
            .html((d.properties.name));
        })
        .on("mouseout", function(d){ maptip.style("display", "none");});


    // Read in background geojson
    var ref_data = FV.mapinfo.ref_data;

    // Add geojson to map
    ref.selectAll("path")
        .data(ref_data.features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("fill", "red");

    // Read in background geojson
    var bg_data = FV.mapinfo.bg_data;

    // Add geojson to map
    bg.selectAll("path")
        .data(bg_data.features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("stroke", "black")
        .style("fill", "#ffffff");


    if (FV.mapinfo.debug) {
        var bbox = svg.append("g");
        var bbox_data = FV.mapinfo.bounds;
        // Add geojson to map
        bbox.selectAll("circle")
        .data(bbox_data.features)
        .enter()
        .append("circle")
        .attr("r", 3)
        .attr("transform", function (d) {
            return "translate(" + projection(d.geometry.coordinates) + ")";
        })
        .attr("class", "debug-point");
    }


});