document.addEventListener("DOMContentLoaded", function (event) {

	"use strict";

	// Map figure 
	var map_options = {'height': FV.mapinfo.height,
						'width': FV.mapinfo.width,
						'proj': proj4(FV.mapinfo.proj4string), 
						'bounds': FV.mapinfo.bounds,
						'scale': FV.mapinfo.scale,
						'bg_data': FV.mapinfo.bg_data,
						'rivers_data': FV.mapinfo.rivers_data,
						'ref_data': FV.mapinfo.ref_data, 
						'site_data': FV.mapinfo.site_data,
						'div_id': '#map'};

	var map_figure = FV.mapmodule(map_options);
	map_figure.init();

	
	/* Hydrograph Setup */

	/**
	 	* Remove/Add accent for a svg circle representing a site.
	 	* Used by hydromodule for cross figure interactions.
	 */
	var site_remove_accent = function(sitekey) {
		var point = document.getElementById('map' + sitekey);
		point.classList.remove('accent');
	}
	var site_add_accent = function(sitekey) {
		var map_site = document.getElementById('map' + sitekey);
		map_site.classList.add('accent');
	}

	var hydro_options = {'height': FV.chart_dimensions.height,
						'width': FV.chart_dimensions.width, 
						'data_path': FV.hydrograph_data_path,
						'div_id' :  '#hydrograph',
						'show_map_tooltip' : map_figure.site_tooltip_show,
						'remove_map_tooltip': map_figure.site_tooltip_remove,
						'site_add_accent' : site_add_accent,
						'site_remove_accent' : site_remove_accent};

	var hydro_figure = FV.hydromodule(hydro_options);
	hydro_figure.init();

});