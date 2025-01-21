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


	const confirmPopupWraper = $("#confirmPopupWraper");
	const confirmMessage = $("#confirmMessage");
	const confirmOk = $("#confirmOk");
	const confirmNo = $("#confirmNo");

	window.confirmation = function (message) {
		return new Promise((resolve) => {
			confirmPopupWraper.addClass("active");

			if (message) {
				confirmMessage.text(message)
			}

			confirmPopupWraper.on('click', function (e) {
				if (e.target === this) {
					confirmNo.click();
				}
			});
			confirmOk.on('click', function (e) {
				confirmPopupWraper.removeClass("active");
				resolve(true);
			})
			confirmNo.on('click', function (e) {
				confirmPopupWraper.removeClass("active");
				resolve(false);
			})
		});
	};
});