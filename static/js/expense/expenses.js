$(document).ready(function () {
	$(document).on('click', '.expense-del', async function (e) {
		let parent = $(this).parent();
		let name = parent.parent().siblings('.expense-description').text();
		let isTrue = await confirmation(`Ви дійсно бажаєте видалити категорию "${name}"?`)

		if (isTrue) {
			$.ajax({
				type: "POST",
				url: $('meta[name="delExpense"]').attr('content'),
				data: {'eID': parent.data('id')},
				success: function (response) {
					load_list()
				}
			});
		}
	})

	$(document).on('click', ".exp-cat-link", function (e) {
		if (!$(e.target).closest('.exp-cat-link-del').length) {
			let link = $(this).find('a').get(0);
			if (link) link.click();
		}
	})

	$(document).on('click', ".exp-plat-link", function (e) {
		if (!$(e.target).closest('.exp-plat-link-del').length) {
			let link = $(this).find('a').get(0);
			if (link) link.click();
		}
	})


	function load_cats() {
		$.ajax({
			type: "GET",
			url: $('.exp-cat-links').data('url'),
			success: function (response) {
				$('.exp-cat-links').html(response.list)
			}
		});
	}
	load_cats()

	function load_plats() {
		$.ajax({
			type: "GET",
			url: $('.exp-plat-links').data('url'),
			success: function (response) {
				$('.exp-plat-links').html(response.list)
			}
		});
	}
	load_plats()


	$(document).on('click', '.exp-cat-link-del', async function (e) {
		let parent = $(this).parent();
		let name = $(this).siblings('a').text();
		let isTrue = await confirmation(`Ви дійсно бажаєте видалити категорию "${name}"?`)
		if (isTrue) {
			$.ajax({
				type: "POST",
				url: $('meta[name="delExpenseCat"]').attr('content'),
				data: {'cID': parent.data('id')},
				success: function (response) {
					load_cats()
				}
			});
		}
	})

	$(document).on('click', '.exp-plat-link-del', async function (e) {
		let parent = $(this).parent();
		console.log(parent.siblings('a').text())
		let name = $(this).siblings('a').text();
		let isTrue = await confirmation(`Ви дійсно бажаєте видалити платформу "${name}"?`)
		if (isTrue) {
			$.ajax({
				type: "POST",
				url: $('meta[name="delExpensePlat"]').attr('content'),
				data: {'cID': parent.data('id')},
				success: function (response) {
					load_plats()
				}
			});
		}
	})
});