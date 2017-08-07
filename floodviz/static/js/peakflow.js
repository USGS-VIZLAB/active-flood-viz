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


	const x = d3.scaleBand().rangeRound([0, width]).padding(.5);

	const y = d3.scaleLinear().range([height, 0]);

	const xAxis = d3.axisBottom().scale(x);
	const yAxis = d3.axisLeft().scale(y).ticks(8);

	var peak_moused_over_bar = {};

	const svg = d3.select('#peakflow_bar').append('svg')
		.attr("preserveAspectRatio", "xMinYMin meet")
		.attr("viewBox", "0 0 " + (width + margin.right) + " " + (height + margin.top + margin.bottom))
		.append('g')
		.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
		.attr('class', 'group');

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

	x.domain(data.map(function (d) {
		return d.label;
	}));
	y.domain([0, d3.max(data, function (d) {
		return d.value;
	})]);

	// Add x axis
	svg.append('g')
		.attr('class', 'axis axis--x')
		.attr('transform', 'translate(0,' + height + ')')
		.call(xAxis)
		.append('text')
		.attr('text-anchor', 'middle')
		.attr('x', (width / 2))
		.attr('y', margin.bottom / 2)
		.text('Year');

	// add y axis
	svg.append('g')
		.attr('class', 'axis axis--y')
		.call(yAxis)
		.append('text')
		.attr('text-anchor', 'middle')
		.attr('transform', 'rotate(-90)')
		.attr('x', 0 - (height / 2))
		.attr('y', 0 - (margin.left / 2))
		.text('Discharge (cfps)');

	// Save last data point as lollipop, and remove it from data
	const lolli_data = data.pop();

	const display_bars = svg.append('g');

	data.forEach(function (d) {
		display_bars.append('rect')
			.attr('class', 'bar')
			.attr('id', 'peak' + d.label)
			.attr('x', function () {
				return x(d.label);
			})
			.attr('y', function () {
				return y(d.value);
			})
			.attr('width', x.bandwidth())
			.attr('height', function () {
				return height - y(d.value);
			});
	});

	const hidden_bars = svg.append('g');

	data.forEach(function (d) {
		hidden_bars.append('rect')
			.attr('class', 'secret-bar')
			.attr('x', function () {
				return x(d.label);
			})
			.attr('y', 0)
			.attr('width', x.padding(0).bandwidth())
			.attr('height', height)
			// tooltip event
			.on('mousemove', function () {
				mouseover(tooltip, d, d3.event)
			})
			.on('mouseout', function () {
				mouseout(tooltip, d)
			});
	});

	// create lollipop Stroke and Circle
	const bars = Array.prototype.slice.call(d3.select('#peakflow_bar svg').selectAll('.bar')['_groups'][0]);
	const last_bars = bars.slice(bars.length - 2).map(function (bar) {
		return bar.x.baseVal.value;
	});
	const padding = last_bars[1] - last_bars[0];

	const lolli_pos_x = ((last_bars[1] + padding + ((1 / 2) * x.bandwidth())).toString());
	const lolli_pos_y = (y(lolli_data['value'])).toString();
	const path_string = 'M ' + lolli_pos_x + ',' + height + ' ' + lolli_pos_x + ',' + lolli_pos_y;
	svg.append('path')
		.attr('id', 'lollipop')
		.attr('stroke-width', 2)
		.attr('d', path_string)
		// tooltip event
		.on('mousemove', function () {
			mouseover(tooltip, lolli_data, d3.event)
		})
		.on('mouseout', function () {
			mouseout(tooltip)
		});

	var group = d3.select('#peakflow_bar svg .group');
	group.append('circle')
		.attr('class', 'cir')
		.attr('r', '4.5')
		.attr('cx', lolli_pos_x)
		.attr('cy', lolli_pos_y)
		.on('mousemove', function () {
			mouseover(tooltip, lolli_data, d3.event)
		})
		.on('mouseout', function () {
			mouseout(tooltip)
		});

	function mouseover(tooltip, d, event) {
		const bar = d3.select('#peak' + d.label);
		bar.attr('class', 'bar-active');
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
		bar.attr('class', 'bar');
		tooltip.style('display', 'none');
	}
});