$(document).ready(function () {
	// active

	// const checkboxAll = $("");
	const editMenuWraper = $(".edit-menu-wraper");
	const editMenuBtn    = $("#editMenuWraperBtn");
	const editMenu       = $("#editMenu");


	function isCheked() {
		for (var check of $(".order_check input")) {
			var isCheked = $(check).is(':checked')
			if (isCheked) {
				editMenuWraper.addClass("active");
				break
			} else {
				editMenuWraper.removeClass("active");
			}
		}
	}
	function getCheked() {
		var li = [];
		$(".order_check input").each(function (i, element) {
			var isCheked = $(element).is(':checked') 
			if (isCheked) {
				li.push($(element).data("id"));
			}
		});
		return li
	}



	$(document).on('change', "#checkbox_all", function (e) {
		var thisIsCheked = $(this).is(':checked')
		$(".order_check input").each(function (i, value) {
			$(value).prop("checked", thisIsCheked)
		});

		isCheked()
	});

	$(document).on('change', ".order_check input", function () {
		isCheked()
	});


	editMenuBtn.on('click', function (e) {
		e.preventDefault();

		if (editMenu.hasClass("active")) {
			editMenu.removeClass("active");
		} else {
			editMenu.addClass("active");
		}
	});




	$(document).on('contextmenu', ".order-block", function(e) {
		e.preventDefault();


		currentContMenu = $(this);

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
		}).show();
	});
	$(document).on('click', function(e) {
		if (!$(e.target).closest('.edit-menu-wraper').length) {
			$('.edit-menu-wraper').hide();
		}
	});

	const delOrders = $("#del_orders");
	const delUrl = $('meta[name="del"]').attr('content')
	
	delOrders.on('click', async function (e) {
		var oList = getCheked()
		var isConfirm = await confirmation(`Ви дійсно бажаєте видалити "${oList.length}" заказів?`);
		if (isConfirm) {
			if (oList) {
				$.ajax({
					type: "GET",
					url: delUrl,
					data: { 'ids': oList.join(',')},
					success: function (response) {
						load_list()
					}
				});
			}
		}
	});
});