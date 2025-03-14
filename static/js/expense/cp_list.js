$(document).ready(function () {
	const LIST = $(".list-cont");

	window.load_list = function () {
		$.ajax({
			type: "GET",
			url: LIST.data('url'),
			success: function (response) {
				LIST.html(response.list)
			}
		});
	}
	load_list()
});