document.addEventListener("DOMContentLoaded", function (event) {

	"use strict";

	// Map figure 
	var map_options = { 'height': FV.mapinfo.height,
						'width': FV.mapinfo.width,
						'proj': proj4(FV.mapinfo.proj4string), 
						'bounds': FV.mapinfo.bounds,
						'scale': FV.mapinfo.scale,
						'bg_data': FV.mapinfo.bg_data,
						'rivers_data': FV.mapinfo.rivers_data,
						'ref_data': FV.mapinfo.ref_data, 
						'site_data': FV.mapinfo.site_data,
						'div_id': '#map'};
	FV.map_figure = FV.mapmodule(map_options);
	FV.map_figure.init();

	
	// Hydrograph 
	var hydro_options = {'height': FV.chart_dimensions.height,
						 'width': FV.chart_dimensions.width, 
						 'data_path': FV.hydrograph_data_path,
						 'div_id' :  '#hydrograph'};
	FV.hydro_figure = FV.hydromodule(hydro_options);
	FV.hydro_figure.init();

});