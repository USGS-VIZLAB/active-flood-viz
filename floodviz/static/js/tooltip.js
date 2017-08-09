'use strict';
const tooltip_module = function (options) {
	var self = {};

	/**
	 * Takes arrow height and the calculated adjustment (to tell whether or not to invert the arrow)
	 * and returns the points-string for the arrow.
	 * @param adjust
	 * @returns a string of points to make up the arrow
	 */
	const make_arrow = function(adjust){
		// sin 60 = sqrt(3)/2 =~ 0.866. Ie, an equilateral triangle of height sqrt(3) will have sides of length 2.
		// So an equilateral triangle with height x will have sides of length x / 0.866
		const sidelength = options.arrowheight / 0.866;

		const points = [[0, 0], [-(sidelength / 2), -adjust.t * options.arrowheight], [(sidelength / 2), -adjust.t * options.arrowheight], [0, 0]];

		// turn points array into string
		var arrowpoints = '';
		points.forEach(function (p) {
			arrowpoints += p[0] + ' ' + p[1] + ',';
		});
		arrowpoints = arrowpoints.substring(0, arrowpoints.length - 1);
		return arrowpoints;
	};

	/**
	 * Calculates what (if any) adjustments are needed to keep the tooltip from running off the sides or top of the svg.
	 *
	 * @param textbound {object} The bounding box around the text
	 * @param center {object} The location of the thing on which the tooltip is centered
	 * @param edges {object} The locations of the edges of the figure, with which the tooltip should not collide
	 *
	 * @returns {{l: number, r: number, t: number}} The left and right adjustment required, and whether or not to draw
	 * the tooltip inverted. See 'EXPLANATION OF `t`' below for more.
	 */
	const calculate_adjust = function(textbound, center, edges){
		// remember that (0, 0) is in the upper left corner
		const tipedges = {
			l: center.x - textbound.width / 2,
			r: center.x + textbound.width / 2,
			t: center.y - textbound.height - options.arrowheight
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
		return adjust;
	};

	/**
	 * Displays the tooltip on a figure.
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


		elements.group.attr('transform', 'translate(' + center.x + ', ' + center.y + ')')
			.attr('class', visible_class);


		// I have to set the text before I can check if it collides with the edges,
		// but I can check if it collides with the top without bumping it up; I only use its height.
		elements.text.html(textstring);

		const textbound = elements.text._groups[0][0].getBBox();

		const adjust = calculate_adjust(textbound, center, edges);

		const arrowpoints = make_arrow(adjust);
		elements.arrow.attr('points', arrowpoints);

		elements.text.attr('y', (-adjust.t * (options.arrowheight + options.padding * 2)));
		/*
		 * The y on the text points to the upper edge, so it requires a bit of adjustment when showing
		 * the tooltip below the gage.
		 * I think this is better than adding some byzantine math to the initial setting.
		 */
		if (adjust.t === -1) {
			var scootdist = parseFloat(elements.text.attr('y'));
			scootdist += textbound.height / 2;
			elements.text.attr('y', scootdist);
		}

		elements.text.attr('transform', 'translate(' + (adjust.l + adjust.r) + ', 0)');
		// One of adjust.l or adjust.r should always be 0.
		elements.backdrop.attr('x', textbound.x - options.padding + adjust.l + adjust.r)
			.attr('y', elements.text.attr('y') - textbound.height + (adjust.t * 0.5))
			.attr('width', textbound.width + options.padding * 2)
			.attr('height', textbound.height + options.padding * 2);
	};
	return self;
};
