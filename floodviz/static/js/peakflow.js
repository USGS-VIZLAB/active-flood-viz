document.addEventListener('DOMContentLoaded', function (event) {

	'use strict';

	var margin = {bottom: 40, right: 40, left: 45, top: 50};
	var width = Math.round(400 * FV.peakmeta['width'] / FV.peakmeta['height']);
	var height = 400;
	var data = FV.peakinfo;

	const scaleX = d3.scaleBand().range([0, width]).padding(.5);
	const scaleY = d3.scaleLinear().range([height, 0]);

	const xAxis = d3.axisBottom().scale(scaleX).tickSizeOuter(0);
	const yAxis = d3.axisLeft().scale(scaleY).ticks(8).tickSizeOuter(0);

	var peak_moused_over_bar = {};

	const svg = d3.select('#peakflow_bar').append('svg')
		.attr("preserveAspectRatio", "xMinYMin meet")
		.attr("viewBox", "0 0 " + (width + margin.right) + " " + (height + margin.top + margin.bottom));

	// All the things added to the graph should be added to this group
	const graph = svg.append('g')
		.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
		.attr('id', 'graph');

	const edges = {
			'l': - margin.left,
			'r': (width + margin.right) - margin.left,
			't': -(margin.top + margin.bottom)
		};


	// For custom X axis ticks
	var ticks = [];
	data.forEach(function (d, i) {
		if (i % 4 === 0) {
			ticks.push(d.label);
		}
	});
	xAxis.tickValues(ticks);

	scaleX.domain(data.map(function (d) {
		return d.label;
	}));
	scaleY.domain([0, d3.max(data, function (d) {
		return d.value;
	})]);

	// Add x axis
	graph.append('g')
		.attr('class', 'axis-x')
		.attr('id', 'peak-axis-x')
		.attr('transform', 'translate(0,' + height + ')')
		.call(xAxis)
		.append('text')
		.attr('text-anchor', 'middle')
		.attr('x', (width / 2))
		.attr('y', margin.bottom / 2)
		.text('Year');

	// add y axis
	graph.append('g')
		.attr('class', 'axis-y')
		.attr('id', 'peak-axis-y')
		.call(yAxis)
		.append('text')
		.attr('text-anchor', 'middle')
		.attr('transform', 'rotate(-90)')
		.attr('x', 0 - (height / 2))
		.attr('y', 0 - (margin.left / 2))
		.text('Discharge (cfps)');

	graph.append("text")
        .attr("x", 0 - margin.left)
        .attr("y", 0 - (margin.top / 2))
        .style("font-size", "14px")
        .text("Discharge (cubic feet per second)");


	const display_bars = graph.append('g');
	const lollipop = graph.append('g')
		.attr('class', 'lollipop');
	const hidden_bars = graph.append('g');

	const peaktip = graph.append('g')
		.attr('id', 'peaktip')
		.attr('class', 'peaktip-hide');
	// I'm abbreviating 'peaktip' to 'pt' in these IDs to clarify that these are in the 'peaktip' group
	peaktip.append('rect')
		.attr('id', 'pt-text-background');
	peaktip.append('polyline')
		.attr('id', 'pt-arrow');
	peaktip.append('text')
		.attr('id', 'pt-text');

	data.forEach(function (d) {
		hidden_bars.append('rect')
			.attr('class', 'secret-bar')
			.attr('x', function () {
				return (scaleX(d.label) - (scaleX.bandwidth() * (scaleX.padding())));
			})
			.attr('y', 0)
			.attr('width', scaleX.copy().padding(0).bandwidth())
			.attr('height', height)
			// tooltip event
			.on('mouseover', function () {
				mouseover(d)
			})
			.on('mouseout', function () {
				mouseout(d)
			});
	});

	// Save last data point as lollipop, and remove it from data
	const lolli_data = data.pop();

	lollipop.attr('id', 'peak' + lolli_data.label);

	data.forEach(function (d) {
		display_bars.append('rect')
			.attr('class', 'bar')
			.attr('id', 'peak' + d.label)
			.attr('x', function () {
				return scaleX(d.label);
			})
			.attr('y', function () {
				return scaleY(d.value);
			})
			.attr('width', scaleX.bandwidth())
			.attr('height', function () {
				return height - scaleY(d.value);
			});
	});


	// This line grabs the list of all the bars, then coerces it into an array
	const bars = Array.prototype.slice.call(d3.select('#peakflow_bar svg').selectAll('.bar')['_groups'][0]);
	// after this, last_bars will contain the x values from the final 2 bars in the array
	const last_bars = bars.slice(bars.length - 2).map(function (bar) {
		return bar.x.baseVal.value;
	});
	const padding = last_bars[1] - last_bars[0];

	// create lollipop Stroke and Circle
	const lolli_pos_x = ((last_bars[1] + padding + ((1 / 2) * scaleX.bandwidth())).toString());
	const lolli_pos_y = (scaleY(lolli_data['value'])).toString();
	const path_string = 'M ' + lolli_pos_x + ',' + height + ' ' + lolli_pos_x + ',' + lolli_pos_y;



	lollipop.append('path')
		.attr('id', 'lollipop-stem')
		.attr('stroke-width', 2)
		.attr('d', path_string);


	lollipop.append('circle')
		.attr('id', 'lollipop-top')
		.attr('r', 4.5)
		.attr('cx', lolli_pos_x)
		.attr('cy', lolli_pos_y);

	function mouseover(d) {
		var center = {
			x: null,
			y: null
		};
		// Find and highlight the bar
		const bar = d3.select('#peak' + d.label);
		if (bar.attr('class').startsWith('lollipop')) {
			bar.attr('class', 'lollipop-active');
			const circle = bar.select('#lollipop-top');
			center = {
				x: parseInt(circle.attr('cx')),
				y: parseInt(circle.attr('cy'))
			}


		}
		else {
			bar.attr('class', 'bar-active');
			const x = parseInt(bar.attr('x'));
			const w = scaleX.bandwidth();
			center = {
				x: x + (w / 2),
				y: parseInt(bar.attr('y'))
			}
		}

		// Assemble elements for tooltip
		const tiptext = peaktip.select('#pt-text');
		const textbg = peaktip.select('#pt-text-background');
		const arrow = peaktip.select('#pt-arrow');
		const tooltip_elements = {
			group: peaktip,
			text: tiptext,
			backdrop: textbg,
			arrow: arrow
		};

		const visible_class = 'peaktip-show';
		const textstring = d.label + ' | ' + d.value + ' cfs';

		FV.show_tooltip(tooltip_elements, textstring, edges, center, visible_class);

		// Only log one hover per bar per session
		if (peak_moused_over_bar[d.label] === undefined) {
			FV.ga_send_event('Peakflow', 'hover_bar', d.label + '_' + d.value);
			peak_moused_over_bar[d.label] = true;
		}
	}

	function mouseout(d) {
		const bar = d3.select('#peak' + d.label);
		if (bar.attr('class').startsWith('lollipop')) {
			bar.attr('class', 'lollipop');
		}
		else {
			bar.attr('class', 'bar')
		}
		peaktip.attr('class', 'peaktip-hide');

	}
});