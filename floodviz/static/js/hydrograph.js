
// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 20, bottom: 30, left: 50};
var width = FV.chartdims.width - margin.left - margin.right;
var height = FV.chartdims.height - margin.top - margin.bottom;

// Set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLog().range([height, 0]);

// Define the line
var line = d3.line()
    .x(function(d) { return x(d.time_mili); })
    .y(function(d) { return y(d.value); });

// Adds the svg canvas
var svg = d3.select("#hydrograph")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

// Get the data
d3.json("../static/data/hydrograph_data.json", function(error, data) {
    data.forEach(function(d) {
        d.value = Number(d.value);
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.time_mili; }));
    y.domain([20, d3.max(data, function(d) { return d.value; })]);

    // Nest the entries by site number
    var dataNest = d3.nest()
        .key(function(d) {return d.key;})
        .entries(data);

    // Loop through each symbol / key
    dataNest.forEach(function(d) {

        svg.append("path")
            .attr("class", "line")
            .attr("id", d.key)
            .attr("d", line(d.values));

    });

    // Add the X Axis
    svg.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add the Y Axis
    svg.append("g")
        .attr("class", "axis")
        .call(d3.axisLeft(y).ticks(10, ".0f"));

});


