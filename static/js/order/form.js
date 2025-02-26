$(document).ready(function () {

	const pageNmae = $('meta[name="page"]').attr('content')
	if (pageNmae == "edit_order") {
		$.each($(".image-preview"), function (i, value) {
			wr = $(value)
			wr.children('img').attr('src', wr.siblings("input").val());
			wr.addClass("active");
		});
	}


	$('#id_product').select2({
		placeholder: 'Выберите продукт',
		allowClear: true
	});

	$("#id_content_type").on('change', function (e) {
		const mID = $(this).val();
		$.ajax({
			type: "GET",
			url: $('meta[name="modelListUrl"]').attr('content'),
			data: { mID: mID },
			success: function (response) {
				var li = []

				$.each(response.models, function (i, element) {
					var el = $('<option>', {
						value: this.id
					}).text(this.name)
					li.push(el)
				});

				$("#id_object_id").html(li)
			}
		});
	})


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

	$('#id_ttn').mask("00 0000 0000 0000", {
		translation: {
			'0': { pattern: /[0-9]/, optional: true }
		},
		placeholder: "0 0000 0000 0000"
	});
});