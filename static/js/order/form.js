$(document).ready(function () {

	const pageNmae = $('meta[name="page"]').attr('content')
	if (pageNmae == "edit_order") {
		$.each($(".image-preview"), function (i, value) {
			wr = $(value)
			wr.children('img').attr('src', wr.siblings("input").val());
			wr.addClass("active");
		});
	}


	const idProduct = $("#id_product");
	idProduct.select2({
		placeholder: 'Выберите продукт',
		allowClear: true
	});


	const imagePreview = $('.image-preview')
	imagePreview.on('click', function (e) {
		e.preventDefault();

		$(this).siblings('input').click();
	});

	$('#id_client_check, #id_bank_check').change(function(e) {
		var reader  = new FileReader();
		var wrapper = $(this).siblings('.image-preview');

		reader.onload = function(e) {
			wrapper.children('img').attr('src', e.target.result);
		}

		reader.readAsDataURL(e.target.files[0]);
		wrapper.addClass("active");
	});


	$('#id_client_phone').mask("+38 (000) 000-00-00");
	$('#id_client_phone').attr("placeholder", "+38 (000) 000-00-00")

	$('#id_ttn').mask("20 0000 0000 0000");
	$('#id_ttn').attr("placeholder", "20 0000 0000 0000");
});