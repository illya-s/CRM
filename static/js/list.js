$(document).ready(function () {
	const LIST = $(".list-cont");
	const PEGI = $("#pagination");
	const URL = LIST.data("url");

	const EPP = $("#EPP");

	const pageName = $('meta[name="page"]').attr('content')

	const EPPN = `${pageName}epp`
	if (!localStorage.getItem(EPPN)) {
		localStorage.setItem(EPPN, 25);
	} else {
		EPP.val(localStorage.getItem(EPPN)).change()
	}
	EPP.change(function (e) {
		localStorage.setItem(EPPN, $(this).val());
		load_list();
	});


	const EPNN = `${pageName}epn`
	if (!localStorage.getItem(EPNN)) {
		localStorage.setItem(EPNN, 1);
	}

	window.load_list = function() {
		if (pageName == "products") {
			$(".pre-product-list").show();
			LIST.hide();
		}

		$.ajax({
			type: "GET",
			url: URL,
			data: { 'page': localStorage.getItem(EPNN), 'epp': localStorage.getItem(EPPN), },
			success: function (response) {
				LIST.html(response.list);
				PEGI.html(response.pagi);

				if (pageName == "products") {
					var img = $('.product-img')

					img[parseInt(img.length) - 1].onload = () => {
						LIST.show();
						$(".pre-product-list").hide();
					};
				}
			},
			error: function (error) {
				alert(`Error: ${error}`)
			}
		});
	}
	load_list()


	$(document).on('click', '.page-link', function () {
		localStorage.setItem(EPNN, $(this).data("page"));
		load_list()
	});
});