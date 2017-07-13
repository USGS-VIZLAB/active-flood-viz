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
	FV.map_figure = FV.mapmodule(map_options);
	FV.map_figure.init();

	
	/* Hydrograph Setup */

	// map interactions for hydrograph events
	var maptip = d3.select('#maptip');
	/**
	 	* Shows/removes sitename tooltip on map figure at correct location.
	 */
	var show_map_tooltip = function(sitename, sitekey) {
		var gage_point_cords = document.getElementById('map'+sitekey).getBoundingClientRect();
		maptip.transition().duration(500);
		maptip.style("display", "inline-block")
			.style("left", (gage_point_cords.left) + 7 + "px")
			.style("top", (gage_point_cords.top - 45) + "px")
			.html((sitename));
	}
	var remove_map_tooltip = function () {
		maptip.style("display", "none");
	}
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
						'show_map_tooltip' : show_map_tooltip,
						'remove_map_tooltip': remove_map_tooltip,
						'site_add_accent' : site_add_accent,
						'site_remove_accent' : site_remove_accent};

	var hydro_figure = FV.hydromodule(hydro_options);
	hydro_figure.init();

});