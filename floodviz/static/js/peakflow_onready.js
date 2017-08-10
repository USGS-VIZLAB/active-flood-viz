document.addEventListener('DOMContentLoaded', function (event) {
	'use strict';

	const tooltip_options = {
		padding: 4,
		arrowheight: 17
	};

	const tooltip = tooltip_module(tooltip_options);
	FV.show_tooltip = tooltip.show_tooltip;
});