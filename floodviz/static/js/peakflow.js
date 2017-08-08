document.addEventListener('DOMContentLoaded', function (event) {

	'use strict';

	const margin = {bottom: 40, right: 40, left: 40, top: 50};
	const width = parseInt(400 * FV.peakmeta['width'] / FV.peakmeta['height']);
	const height = 400;
	var data = FV.peakinfo;

	// Collect and set peakflow bar chart aspect ratio data
	var peakflow_bar = document.getElementById('peakflow_bar');
	peakflow_bar.style.height = height;
	peakflow_bar.style.width = width;


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

	const tooltip = d3.select('body')
		.append('div')
		.attr('class', 'toolTip');

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


	const display_bars = graph.append('g');
	const lollipop = graph.append('g')
		.attr('class', 'lollipop');
	const hidden_bars = graph.append('g');

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
				mouseover(tooltip, d, d3.event)
			})
			.on('mouseout', function () {
				mouseout(tooltip, d)
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

	function mouseover(tooltip, d, event) {
		const bar = d3.select('#peak' + d.label);
		if (bar.attr('class').startsWith('lollipop')) {
			bar.attr('class', 'lollipop-active');
		}
		else {
			bar.attr('class', 'bar-active');
		}
		tooltip.transition().duration(500).style('opacity', .9);
		tooltip.style('display', 'inline-block')
			.style('left', (event.pageX) + 10 + 'px')
			.style('top', (event.pageY - 70) + 'px')
			.html((d.label) + '<br>' + (d.value) + ' cfs');

		// Only log one hover per bar per session
		if (peak_moused_over_bar[d.label] === undefined) {
			FV.ga_send_event('Peakflow', 'hover_bar', d.label + '_' + d.value);
			peak_moused_over_bar[d.label] = true;
		}
	}

	function mouseout(tooltip, d) {
		const bar = d3.select('#peak' + d.label);
		if (bar.attr('class').startsWith('lollipop')) {
			bar.attr('class', 'lollipop');
		}
		else {
			bar.attr('class', 'bar')
		}
		tooltip.style('display', 'none');

	}
});