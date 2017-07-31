document.addEventListener('DOMContentLoaded', function (event) {
	'use strict';

	// Map options
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
	// Hydrograph options
	var hydro_options = {
		'height': FV.hydrograph_dimensions.height,
		'width': FV.hydrograph_dimensions.width,
		'div_id': '#hydrograph'
	};

	var map_figure = FV.mapmodule(map_options);
	var hydro_figure = FV.hydromodule(hydro_options);

	// Use frames to link interactions
	var map_to_hydro = {
		'hover_in': map_figure.site_tooltip_show,
		'hover_out': map_figure.site_tooltip_remove,
		'click': map_figure.site_remove_accent,
		'accent_on_map': map_figure.site_add_accent
	};
	var hydro_to_map = {
		'hover_in': hydro_figure.activate_line,
		'hover_out': hydro_figure.deactivate_line,
		'click': hydro_figure.change_lines
	};

	map_figure.init(hydro_to_map);
	//data for hydrograph
	d3.json(FV.hydrograph_data_path, function (error, data) {
		if (error) { console.error(error); }
		hydro_options['data'] = data;
		hydro_figure.init(map_to_hydro);
	});
});