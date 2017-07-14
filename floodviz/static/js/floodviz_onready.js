document.addEventListener("DOMContentLoaded", function (event) {
	"use strict";

	/**
	 * Update the value of display_ids and call update to redraw the graph to match.
	 * @param new_display_ids The new set of gages to be displayed.
	 */
	var change_lines = function (new_display_ids) {
		display_ids = new_display_ids;
		var new_data = full_data.filter(function (d) {
			return display_ids.indexOf(d.key !== -1);
		});
		update(new_data);
	};


	// Map figure
	var map_options = {
		'height': FV.mapinfo.height,
		'width': FV.mapinfo.width,
		'proj': proj4(FV.mapinfo.proj4string),
		'bounds': FV.mapinfo.bounds,
		'scale': FV.mapinfo.scale,
		'bg_data': FV.mapinfo.bg_data,
		'rivers_data': FV.mapinfo.rivers_data,
		'ref_data': FV.mapinfo.ref_data,
		'site_data': FV.mapinfo.site_data,
		'div_id': '#map'
	};

	var map_figure = FV.mapmodule(map_options);
	map_figure.init();


	/* Hydrograph Setup */
	/**
	 * Remove/Add accent for a svg circle representing a site.
	 * Used by hydromodule for cross figure interactions.
	 */
	var site_remove_accent = function (sitekey) {
		d3.select('#map' + sitekey).attr('class', 'gage-point');
	};
	var site_add_accent = function (sitekey) {
		d3.select('#map' + sitekey).attr('class', 'gage-point-accent');
	};

	var hydro_options = {
		'height': FV.hydrograph_dimensions.height,
		'width': FV.hydrograph_dimensions.width,
		'data_path': FV.hydrograph_data_path,
		'div_id': '#hydrograph',
		'show_map_tooltip': map_figure.site_tooltip_show,
		'remove_map_tooltip': map_figure.site_tooltip_remove,
		'site_add_accent': site_add_accent,
		'site_remove_accent': site_remove_accent
	};

	var hydro_figure = FV.hydromodule(hydro_options);
	hydro_figure.init();

});