$(document).ready(function () {
	const LIST = $(".list-cont");
	const URL = LIST.data("url");


	window.load_list = function() {
		$.ajax({
			type: "GET",
			url: URL,
			success: function (response) {
				LIST.html(response.list);
			},
			error: function (error) {
				alert(`Error: ${error}`)
			}
		});
	}
	load_list()
});