
d3.json('..\\static\\data\\hydrograph_data.json', function(data) {  // open more dynamic file path

  nv.addGraph( function() {
    
    var chart = nv.models.cumulativeLineChart()
                  .x( function(d) {return d.time_mili})  // this value is stored in miliseconds since epoch (converted in data_format.py with datetime)
                  .y( function(d) {return d.value * 1000}) // TODO: seems to show up wrong on chart
                  .color(d3.scale.category10().range())
                  .useInteractiveGuideline(true)
                  ;

    chart.xAxis
        .axisLabel(" Date ")
        .ticks(5)
        .tickFormat(function(d) {
            return d3.time.format('%y-%d-%m')(new Date(d))
        });

    chart.yAxis
        .axisLabel('Discharge (cubic feet per second)')
        .tickFormat(function(d) { return d3.format(",")(d) + " cfps"})
    
    d3.select('#hydrograph svg')
        .datum(data)
        .call(chart);

    //TODO: Figure out a good way to do this automatically
    nv.utils.windowResize(chart.update);
    return chart;
  });

});
