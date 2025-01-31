$(document).ready(function () {
	var currentContMenu;

	$(document).on('contextmenu', ".expense-block", function(e) {
		e.preventDefault();

		currentContMenu = $(this).data('id');

		var menuWidth = $('#custom-menu').outerWidth();
		var menuHeight = $('#custom-menu').outerHeight();
		
		var windowWidth = $(window).width();
		var windowHeight = $(window).height();
		
		var mouseX = e.pageX;
		var mouseY = e.pageY;
		
		if (mouseX + menuWidth > windowWidth) {
			mouseX = windowWidth - menuWidth;
		}
		
		if (mouseY + menuHeight > windowHeight) {
			mouseY = windowHeight - menuHeight;
		}


		$('.edit-menu-wraper').css({
			top: mouseY + "px",
			left: mouseX + "px",
		}).addClass('active');
	});
	$(document).on('click', function(e) {
		if (!$(e.target).closest('.edit-menu-wraper').length) {
			$('.edit-menu-wraper').removeClass('active');
		}
	});


	$('.upd-menu-btn').on('click', function (e) {
		window.location.href = `${window.location.origin}${$('meta[name="updExpense"]').attr('content')}?eID=${currentContMenu}`
		$('.edit-menu-wraper').removeClass('active');
	})
	$('.del-menu-btn').on('click', function (e) {
		$.ajax({
			type: "POST",
			url: $('meta[name="delExpense"]').attr('content'),
			data: {'eID': currentContMenu},
			success: function (response) {
				load_list()
			}
		});
		$('.edit-menu-wraper').removeClass('active');
	})
});