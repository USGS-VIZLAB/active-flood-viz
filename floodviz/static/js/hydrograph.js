
d3.json('..\\static\\data\\hydrograph_data.json', function(data) {  // open more dynamic file path

  nv.addGraph( function() {
    
    var getX = function(d) { return d.time_mili }
    var getY = function(d) { return d.value }
    var getMax = function(d) { return d.max }

    var min = d3.min(data, function(d) { return d3.min(d.values, getY)})
    var max = d3.max(data, function(d) { return d3.max(d.values, getMax)})
    
    var chart = nv.models.cumulativeLineChart()
                  .x( getX )  // this value is stored in miliseconds since epoch (converted in data_format.py with datetime)
                  .y( getY ) 
                  .color(d3.scale.category10().range())
                  .useInteractiveGuideline(true)
                  .yDomain([min, max])
                  .margin({left: 120, top: 60})
                  .showControls(false)
                  ;

    chart.xAxis
        .axisLabel(" Date (Y-D-M)")
        .axisLabelDistance(10)
        .ticks(5)
        .tickFormat(function(d) {
            return d3.time.format('%y-%d-%m')(new Date(d))
        });

    chart.yAxis
        .axisLabel('Discharge (cubic feet per second)')
        .axisLabelDistance(40)
        .ticks(5)
        .tickFormat(function(d) { return d3.format(",")(d) + " cfps"});
    
    d3.select('#hydrograph svg')
        .datum(data)
        .call(chart);

    //TODO: Figure out a good way to do this automatically
    nv.utils.windowResize(chart.update);
    return chart;
  });

});
