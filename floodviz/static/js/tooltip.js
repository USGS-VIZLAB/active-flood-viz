'use strict';
const tooltip_module = function (options) {
	var self = {};
	/**
	 *
	 * @param elements {Object} containing pointers to the SVG elements used in the tooltip:
	 *    group: the group containing the other tooltip elements
	 *    text: the text to be shown
	 *    backdrop: the rectangle used as a background for the text
	 *    arrow: the triangle thing
	 *
	 * @param textstring {string} the text to be used in the tooltip
	 * @param edges {object} of the form {r: , l: , t: } giving the  right, left, and top edges of the figure
	 * @param center {object} of the form {x: , y: } giving the SVG coordinates to be used as the center of the tooltip.
	 * @param visible_class {string} the name of the class to which the tooltip is set to make it visible
	 */
	self.show_tooltip = function (elements, textstring, edges, center, visible_class) {
		const padding = 4;
		const arrowheight = 17;
		// sin 60 = sqrt(3)/2 =~ 0.866. Ie, an equilateral triangle of height sqrt(3) will have sides of length 2.
		// So an equilateral triangle with height x will have sides of length x / 0.866
		const sidelength = arrowheight / 0.866;


		elements.group.attr('transform', 'translate(' + center.x + ', ' + center.y + ')')
			.attr('class', visible_class);


		// I have to set the text before I can check if it collides with the edges,
		// but I can check if it collides with the top without bumping it up; I only use its height.
		elements.text.html(textstring);

		const textbound = elements.text._groups[0][0].getBBox();

		// remember that (0, 0) is in the upper left corner
		const tipedges = {
			l: center.x - textbound.width / 2,
			r: center.x + textbound.width / 2,
			t: center.y - textbound.height - arrowheight
		};

		/*
		* EXPLANATION OF `t`.
		* t for Top. This is set to -1 to draw the tooltip under the gage rather than above it.
		* In many places I was negating positive values (eg -x) before use to yield and upward offset.
		* In those places I now use (-t * x) to achieve an upward offset when t = 1
		* and a downward offset when t = -1.
		*/
		var adjust = {
			'l': 0,
			'r': 0,
			't': 1
		};

		if (tipedges.l < edges.l) {
			// this will be positive so it will be a shift to the right
			adjust.l = edges.l - tipedges.l
		}
		else if (tipedges.r > edges.r) {
			// this will be negative, so a shift to the left
			adjust.r = edges.r - tipedges.r
		}
		if (tipedges.t < edges.t) {
			// set t to -1 so that the tooltip will bw drawn under the gage.
			adjust.t = -1
		}

		const points = [[0, 0], [-(sidelength / 2), -adjust.t * arrowheight], [(sidelength / 2), -adjust.t * arrowheight], [0, 0]];

		// turn points array into string
		var arrowpoints = '';
		points.forEach(function (p) {
			arrowpoints += p[0] + ' ' + p[1] + ',';
		});
		arrowpoints = arrowpoints.substring(0, arrowpoints.length - 1);

		elements.arrow.attr('points', arrowpoints);

		elements.text.attr('y', (-adjust.t * (arrowheight + padding * 2)));
		/*
		 * The y on the text points to the upper edge, so it requires a bit of adjustment when showing
		 * the tooltip below the gage.
		 * I think this is better than adding some byzantine math to the initial setting.
		 */
		if (adjust.t === -1) {
			var scootdist = parseFloat(tiptext.attr('y'));
			scootdist += textbound.height / 2;
			elements.text.attr('y', scootdist);
		}

		elements.text.attr('transform', 'translate(' + (adjust.l + adjust.r) + ', 0)');
		// One of adjust.l or adjust.r should always be 0.
		elements.backdrop.attr('x', textbound.x - padding + adjust.l + adjust.r)
			.attr('y', elements.text.attr('y') - textbound.height + (adjust.t * 0.5))
			.attr('width', textbound.width + padding * 2)
			.attr('height', textbound.height + padding * 2);
	};
	return self;
};
