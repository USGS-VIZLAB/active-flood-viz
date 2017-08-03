(function (i, s, o, g, r, a, m) {
	i['GoogleAnalyticsObject'] = r;
	i[r] = i[r] || function () {
			(i[r].q = i[r].q || []).push(arguments)
		}, i[r].l = 1 * new Date();
	a = s.createElement(o),
		m = s.getElementsByTagName(o)[0];
	a.async = 1;
	a.src = g;
	m.parentNode.insertBefore(a, m)
})(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-103831764-1', 'auto');
ga('send', 'pageview');


// GA for DOM content not related to figures.
document.addEventListener('DOMContentLoaded', function (event) {
	// External links clicked
	var links = document.getElementsByTagName("a");
	Array.prototype.forEach.call(links, function (element) {
		element.addEventListener('click', function () {
			ga_send_event('Links', 'click_link', element.href);
		});
	});

});
