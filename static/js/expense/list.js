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

	window.load_list = function() {
		var y = $("#yearSelect").val()
		var m = $("#monthSelect").val()
		var d = $("#daySelect").val()
		var cat = $("#catSelect").val()
		var plat = $("#platSelect").val()

		var context = {
			'page': params.get("p"),
			'epp': params.get("epp"),
			'cp': cat && plat ? `${cat},${plat}` : undefined,
			'ymd': y && m ? `${y},${m},${d}`: undefined
		}

		$.ajax({
			type: "GET",
			url: URL,
			data: context,
			success: function (response) {
				LIST.html(response.list);

				const yearSelect  = $("#yearSelect");
				const monthSelect = $("#monthSelect");
				const daySelect   = $("#daySelect");
				const catSelect   = $("#catSelect");
				const platSelect  = $("#platSelect");

				yearSelect.html()
				monthSelect.html()
				daySelect.html()


				monthSelect.append(
					$('<option>', {value: "-1"}).text("Все")
				)
				daySelect.append(
					$('<option>', {value: "-1"}).text("Все")
				)


				$(response.yl).each(function (i, element) {
					var el = $('<option>', {value: element}).text(element)
					yearSelect.append(el)
				});
				$(response.ml).each(function (i, element) {
					var el = $('<option>', {value: element}).text(element)
					monthSelect.append(el)
				});
				$(response.dl).each(function (i, element) {
					var el = $('<option>', {value: element}).text(element)
					daySelect.append(el)
				});

				yearSelect.val(response.cy)
				monthSelect.val(response.cm)
				daySelect.val(response.cd)

				catSelect.val(response.cCat)
				platSelect.val(response.cPlat)

				$("#EPP").val($("#EPP").data('epp'))
			},
			error: function (error) {
				alert(`Error: ${error}`)
			}
		});
	}
	load_list()

	window.load_filters = function () {
		$.ajax({
			type: "GET",
			url: $('.filter-wraper').data('url'),
			success: function (response) {
				$('.filter-wraper').html(response.list)
			}
		});
	}
	load_filters()

	$(window).on("hashchange", function() {
		load_list()
	});

	$(document).on('change', '#yearSelect, #monthSelect, #daySelect, #catSelect, #platSelect', function (e) {
		load_filters()
		load_list()
	})

	$(document).on('click', '.page-link', function () {
		params.set("p", $(this).data("page"));
		window.history.replaceState(null, null, "?" + params.toString() + window.location.hash);
		load_list()
	});
});