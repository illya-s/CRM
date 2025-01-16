$(document).ready(function () {
	const page_name = $('meta[name="page_name"]').attr('content');

	var links = $('nav').find('a');
	links.each(function (i, el) {
		if ($(this).data('id') == page_name) {
			$(this).addClass('active');
			$(this).attr("disabled", "disabled").css("pointer-events", "none")
		}
	});

	$('#showNavBar, #closeNavBar').on('click', function (e) {
		$('nav').toggleClass('active');
	})
});