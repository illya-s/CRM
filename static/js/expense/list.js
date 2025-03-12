$(document).ready(function () {
	const LIST = $(".list-cont");
	// const PEGI = $("#pagination");
	const URL = LIST.data("url");


	let params = new URLSearchParams(window.location.search);

	if (!params.get("p")) {
		params.set("p", "1");
		window.history.replaceState(null, null, "?" + params.toString() + window.location.hash);
	}
	if (!params.get("epp")) {
		params.set("epp", "25");
		window.history.replaceState(null, null, "?" + params.toString() + window.location.hash);
	}

	$(document).on('change', "#EPP", function (e) {
		params.set("epp", $(this).val());
		window.history.replaceState(null, null, "?" + params.toString() + window.location.hash);
		load_list();
	});

	function hash() {
		return window.location.hash.split("#")[1]
	}

	if (hash() == "" || hash() == undefined) {
		window.location.hash = "-1"
	}

	window.load_list = function() {
		var y = $("#yearSelect").val()
		var m = $("#monthSelect").val()
		var d = $("#daySelect").val()
		$.ajax({
			type: "GET",
			url: URL,
			data: { 'page': params.get("p"), 'epp': params.get("epp"), 'filter': hash(), 'ymd': y && m ? `${y},${m},${d}`: undefined },
			success: function (response) {
				LIST.html(response.list);
				$("#EPP").val($("#EPP").data('epp'))
			},
			error: function (error) {
				alert(`Error: ${error}`)
			}
		});
	}
	load_list()

	$(window).on("hashchange", function() {
		load_list()
	});

	$(document).on('change', '#yearSelect, #monthSelect, #daySelect', function (e) {
		load_list()
	})

	$(document).on('click', '.page-link', function () {
		params.set("p", $(this).data("page"));
		window.history.replaceState(null, null, "?" + params.toString() + window.location.hash);
		load_list()
	});
});