function close_dialogs(){
	$('.future_dialog').dialog('close');
}

$(function(){

	if ($LOGGED_IN == 'True'){
		var add_painting_dialog;

		var edit_painting_dialog;

		var add_painting_options = {
			beforeSubmit: function(formData, jqForm, options){
				var queryString = $.param(formData);
				console.log('About to submit: ' + queryString);
			},
			success: function(responseText, statusText, xhr, $form){
				console.log(responseText);
				$('#paintings').append(responseText.content);
				add_painting_dialog.dialog('close');
			},
			url: $SCRIPT_ROOT + '/ajax/add_painting',
			type: 'post',
			dataType: 'json'
		};

		var edit_painting_options = {
			beforeSubmit: function(formData, jqForm, options){
				var queryString = $.param(formData);
				console.log('About to submit: ' + queryString);
			},
			success: function(responseText, statusText, xhr, $form){
				var painting_to_edit = $('.image_container[image_id=' + responseText.image_id + ']');
				painting_to_edit.replaceWith(responseText.content);
				edit_painting_dialog.dialog('close');
			},
			url: $SCRIPT_ROOT + '/ajax/edit_painting',
			type: 'post',
			dataType: 'json'
		};

		var sort_paintings = {
			update: function(event,ui){
				var order = $( "#paintings" ).sortable('serialize', {attribute: 'sort_id', key: 'image[]'});
				$.ajax({
					type: 'POST',
					url: $SCRIPT_ROOT + '/ajax/update_paintings_order',
					data: order
				}).done(function(response){
					console.log(response);
				}).fail(function(error){
					show_message(error, true);
			});
			}
		};

		$('#paintings').sortable(sort_paintings);
			// other available options: 
			//clearForm: true        // clear all form fields after successful submit 
			//resetForm: true        // reset the form after successful submit 
			//timeout:   3000 


		$('body').on('click', '.add_painting_button', function(){
			close_dialogs();
			console.log('add_painting_button was pressed');
			add_painting_dialog = $('.add_painting_div').clone();
			add_painting_dialog.addClass('future_dialog');
			add_painting_dialog.dialog(
				{
					create: function(){
						$('.add_painting_div form').ajaxForm(add_painting_options);
					},
					modal: true,
					close: function(){
						$(this).remove();
					},
					overlay: {
						backgroundColor: '#000',
						opacity: 0.5
					}
				});
			$('.add_painting_div').attr('display', 'block');
		});

		$('body').on('click', '.delete_painting_button', function(){
			close_dialogs();
			var id = $(this).attr('image_id');
			$.ajax({
				type: 'POST',
				url: $SCRIPT_ROOT + '/ajax/delete_painting',
				data: {image_id: id}
			}).done(function(response){
				console.log(response);
				$('.image_container[image_id=' + id + ']').remove();
			}).fail(function(error){
				show_message(error, true);
			});
		});

		$('body').on('click', '.edit_painting_button', function(){
			close_dialogs();
			var id = $(this).attr('image_id');
			$.ajax({
				type: 'POST',
				url: $SCRIPT_ROOT + '/ajax/editing_form',
				data: {image_id: id}
			}).done(function(response){
				console.log(response);
				$('body').append(response.content);
				var editing_form_options = {
					close: function(event, ui){
						$('.edit_painting_div[image_id=' + id + ']').remove();
					}
				};
				edit_painting_dialog = $('.edit_painting_div[image_id=' + id + ']');
				edit_painting_dialog.addClass('future_dialog');
				edit_painting_dialog.dialog(editing_form_options);
				$('.edit_painting_div form').ajaxForm(edit_painting_options);
			}).fail(function(error){
				show_message(error, true);
			});
		});


		//Posts
		var add_post_dialog;
		var edit_post_dialog;


		var add_post_options = {
			beforeSubmit: function(formData, jqForm, options){
				var queryString = $.param(formData);
				console.log('About to submit: ' + queryString);
			},
			success: function(responseText, statusText, xhr, $form){
				console.log(responseText);
				$('#posts').append(responseText.content);
				add_post_dialog.dialog('close');
			},
			url: $SCRIPT_ROOT + '/ajax/add_post',
			type: 'post',
			dataType: 'json'
		};

		var edit_post_options = {
			beforeSubmit: function(formData, jqForm, options){
				var queryString = $.param(formData);
				console.log('About to submit: ' + queryString);
			},
			success: function(responseText, statusText, xhr, $form){
				console.log(responseText);
				var post_to_edit = $('.post_container[post_id=' + responseText.post_id + ']');
				post_to_edit.replaceWith(responseText.content);
				edit_post_dialog.dialog('close');
			},
			url: $SCRIPT_ROOT + '/ajax/edit_post',
			type: 'post',
			dataType: 'json'
		};

		$('body').on('click', '.add_post_button', function(){
			close_dialogs();
			console.log('add_post_button was pressed');
			add_post_dialog = $('.add_post_div').clone();
			add_post_dialog.addClass('future_dialog');
			add_post_dialog.dialog(
				{
					modal: true,
					create: function(){
						$('.add_post_div form').ajaxForm(add_post_options);
					},
					close: function(){
						$(this).remove();
					},
					overlay: {
						backgroundColor: '#000',
						opacity: 0.5
					}
				});
			$('.add_post_div').attr('display', 'block');
		});

		$('.add_post_div form').ajaxForm(add_post_options);

		$('body').on('click', '.edit_post_button', function(){
			close_dialogs();
			var id = $(this).attr('post_id');
			console.log(id);
			$.ajax({
				type: 'POST',
				url: $SCRIPT_ROOT + '/ajax/editing_post_form',
				data: {post_id: id}
			}).done(function(response){
				console.log(response);
				$('body').append(response.content);
				var editing_post_form_options = {
					close: function(event, ui){
						$('.edit_post_div[post_id=' + id + ']').remove();
					}
				};
				edit_post_dialog = $('.edit_post_div[post_id=' + id + ']');
				edit_post_dialog.addClass('future_dialog');
				edit_post_dialog.dialog(editing_post_form_options);
				$('.edit_post_div form').ajaxForm(edit_post_options);
			}).fail(function(error){
				show_message(error, true);
			});
		});

		$('body').on('click', '.delete_post_button',  function(){
			close_dialogs();
			var id = $(this).attr('post_id');
			$.ajax({
				type: 'POST',
				url: $SCRIPT_ROOT + '/ajax/delete_post',
				data: {post_id: id}
			}).done(function(response){
				console.log(response);
				$('.post_container[post_id=' + id + ']').remove();
			}).fail(function(error){
				show_message(error, true);
			});
		});

	}


	else{
		$('.show_description_link').on('click', function(){
		var id = $(this).attr('image_id');
		$.ajax({
			type: 'POST',
			url: $SCRIPT_ROOT + '/ajax/get_description',
			data: {image_id: id}
		}).done(function(response){
			$('#description_container').html(response.content);
			console.log(response);
		});
		return false;
		});
	}
});

function show_message(message, error){
	console.log(message);
}