document.addEventListener("DOMContentLoaded", function (event) {

	"use strict";

	// Map figure setup
	var map_height = FV.mapinfo.height;
	var map_width = FV.mapinfo.width;
	var proj = proj4(FV.mapinfo.proj4string);
	var bounds = FV.mapinfo.bounds;
	var scale = FV.mapinfo.scale;
	var bg_data = FV.mapinfo.bg_data;
	var rivers_data = FV.mapinfo.rivers_data;
	var ref_data = FV.mapinfo.ref_data;
	var site_data = FV.mapinfo.site_data;
	var map_options = { 'height': map_height, 'width': map_width, 'proj': proj, 'bounds': bounds, 'scale': scale,
						'bg_data': bg_data, 'rivers_data': rivers_data, 'ref_data': ref_data, 'site_data': site_data }
	// create figure from options
	FV.map_figure = FV.mapmodule(map_options);
	FV.map_figure.init();

	
	// Hydrograph figure setup
	var hydro_height = FV.chart_dimensions.height;
	var hydro_width = FV.chart_dimensions.width;
	var hydro_data_path = FV.hydrograph_data_path;
	var hydro_options = {'height': hydro_height, 'width': hydro_width, 'data_path':hydro_data_path}
	// create figure from options
	FV.hydro_figure = FV.hydromodule(hydro_options);
	FV.hydro_figure.init();

});