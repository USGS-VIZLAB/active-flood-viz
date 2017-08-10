document.addEventListener('DOMContentLoaded', function (event) {
	'use strict';

	const tooltip_options = {
		padding: 4,
		arrowheight: 17
	};

	const tooltip = tooltip_module(tooltip_options);
	FV.show_tooltip = tooltip.show_tooltip;

	// Map options
	var map_options = {
		'disableInteractions': true,
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
});