document.addEventListener("DOMContentLoaded", function (event) {
    "use strict";
    var proj4string = FV.mapinfo.proj4string;
    var proj = proj4(proj4string);

    function degreesToRadians(degrees) {
        return degrees * Math.PI / 180;
    }

    function radiansToDegrees(radians) {
        return radians * 180 / Math.PI;
    }

    var project = function (lambda, phi) {
        return proj.forward([lambda, phi].map(radiansToDegrees));
    };

    project.invert = function (x, y) {
        return proj.inverse([x, y]).map(degreesToRadians);
    };

    //Define map projection
    var projection = d3.geoProjection(project);
    projection.scale(1)
        .translate([0, 0]);


    //Define path generator
    var path = d3.geoPath().projection(projection);

    var height = FV.mapinfo.height;
    var width = FV.mapinfo.width;

    //Create SVG element
    var svg = d3.select("body")
        .append("svg")
        .attr("width", width)
        .attr("height", height);


    var bg = svg.append("g"),
        sites = svg.append("g");


    var site_data = FV.mapinfo.site_data;
    // Calculate bounding box transforms for entire collection
    var b = path.bounds(site_data);
    var s = .95 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height);
    var t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2];

    // Update the projection
    projection
        .scale(s)
        .translate(t);

    var bg_data = FV.mapinfo.bg_data;
    bg.selectAll("path")
        .data(bg_data.features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("stroke", "black")
        .style("fill", "#ffffff");



    //Bind data and create one path per GeoJSON feature
    sites.selectAll("path")
        .data(site_data.features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("fill", "blue");




});