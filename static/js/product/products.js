$(document).ready(function () {
	const searchInput = $("#searchProduct");
	const searchBtn = $("#searchBtn");

	const LIST = $(".list-cont");
	const PEGI = $("#pagination");

	const EPP = $("#EPP");

	const pageNameTag = $('meta[name="page"]');

	const EPPN = `${pageNameTag.attr('content')}epp`
	if (!localStorage.getItem(EPPN)) {
		localStorage.setItem(EPPN, 25);
	} else {
		EPP.val(localStorage.getItem(EPPN)).change()
	}
	EPP.change(function (e) {
		localStorage.setItem(EPPN, $(this).val());
		load_list();
	});


	const EPNN = `${pageNameTag.attr('content')}epn`
	if (!localStorage.getItem(EPNN)) {
		localStorage.setItem(EPNN, 1);
	}

	var query;

	window.load_list = function() {
		$.ajax({
			type: "GET",
			url: LIST.data('url'),
			data: {
				'page': localStorage.getItem(EPNN),
				'epp': localStorage.getItem(EPPN),
				'q': query
			},
			success: function (response) {
				LIST.html(response.list);
				PEGI.html(response.pagi);
			},
			error: function (error) {
				alert(`Error: ${error}`)
			}
		});
	}

	$('.supplier-products').on('click', function (e) {
		var url = $(this).data('url');
		LIST.data('url', url)
		load_list()
	})

	$(document).on('click', '.page-link', function () {
		localStorage.setItem(EPNN, $(this).data("page"));
		load_list()
	});

	searchInput.on('input', function (e) {
		query = $(this).val()
	});
	searchInput.on('keypress', function (e) {
		if (e.which == 13) {
			searchBtn.click()
		}
	});
	searchBtn.on('click', function (e) {
		load_list()
	})
});