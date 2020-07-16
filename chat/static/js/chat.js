function deleteMessage(id){
	$.ajax({
		url: '/chat/api/message/'+id+'/',
		type: 'DELETE',
		headers : {"X-CSRFToken":$.cookie("csrftoken")}
	})
	.done(function() {
		$("#message"+id).remove(); 
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});   
}

jQuery(document).ready(function($) {

	function templMyMsg(id, content, time){
		time = time.split("T")[1].split('.')[0].slice(0,-3)
		return `
<div class="makeStyles-root-367 mt-1 makeStyles-authUser-368" id="message${id}">
	<div class="makeStyles-inner-369">
		<a class="MuiAvatar-root makeStyles-avatar-370">${$("#userDropdown").html()}</a>
		<div>
			<div class="makeStyles-body-371">
				<div>
					<a class="font-weight-bold small">Me</a>
					<button class="btn btn-link float-right deleteMessage"
						data-id="${id}">
						<i class="fas fa-times text-danger" style="float: right;"></i>
					</button>
				</div>
				<div
				<p class="mb-0 MuiTypography-root MuiTypography-body1 MuiTypography-colorInherit">${content}</p>
			</div>
		</div>
		<div class="makeStyles-footer-374">
			<p class="mb-0 MuiTypography-root MuiTypography-body2">${time}</p>
		</div>
	</div>
</div>
</div>
		`
	}

	function templOthersMsg(id, source_name, sender_div, content, time){
		div_img = sender_div.find('.MuiListItemAvatar-root').html();
		time = time.split("T")[1].split('.')[0].slice(0,-3)
		return `
<div class="makeStyles-root-367 mt-1" id="message${id}">
	<div class="makeStyles-inner-369">
		<a class="MuiAvatar-root makeStyles-avatar-370">${div_img}</a>
		<div>
			<div class="makeStyles-body-371">
				<div>
					<a class="font-weight-bold small">${source_name}</a>
				</div>
				<div
				<p class="mb-0 MuiTypography-root MuiTypography-body1 MuiTypography-colorInherit">${content}</p>
			</div>
		</div>
		<div class="makeStyles-footer-374">
			<p class="mb-0 MuiTypography-root MuiTypography-body2">${time}</p>
		</div>
	</div>
</div>
</div>
		`
	}

	function scrollDown(){
		div = $("#messages_boddy").parent(".bd-content");
// div.scrollTop(div.prop("scrollHeight"));
div.animate({ scrollTop: div.prop("scrollHeight")}, 100);
}

$("#form_message_file").on('change', function(event) {
	event.preventDefault();
	filename = $(this).val().replace(/.*(\/|\\)/, '');
	$('#form_message_text').val(filename);
});

loc = window.location;
w_start = "ws://";
if(loc.protocol==="https:"){
	w_start = "wss://";
}
ws_url = w_start+loc.host+loc.pathname;

socket = new WebSocket(ws_url);

socket.onmessage = function(e){
	data = JSON.parse(e.data);
	console.log(data.type, data.message);
	if(String(data.type) === "deletion"){
		div_id = "#message"+data.message;
		$div_message = $(div_id);
		$div_message.remove();
	}else{
		sender_div = $("#contact"+data.source);

		sender_pic = sender_div.find('.MuiAvatar-img').attr('src');
		sender_name = sender_div.find('.contact_fullname').text();
		unread_count = sender_div.find('.unread_count');

		if(unread_count.text().trim().length < 1){
			unread_count.text(1);
		}else{
			unread_count.text(parseInt(unread_count.text())+1);
		}
		sender_div.find('.txt_last_msg').text(data.message);
		sender_div.find('.txt_last_msg_time').text(data.timestamp.split("T")[1].split('.')[0].slice(0,-3));

		if(String(data.source) == String($("#destination").val())){
			$("#messages_boddy").append(templOthersMsg(data.id, sender_name, sender_div, data.message, data.timestamp));
		}
	}
	scrollDown();
};
socket.onopen = function(e){
	console.log("socket open", e);
	$("#form_message").on('submit', function(event){
		event.preventDefault();
		event.stopPropagation();
		$form = $(this);
		$.ajax({
			url: '/chat/api/message/',
			type: 'POST',
			data: new FormData(this),
			processData: false,
			contentType: false,
			cache: false,
			headers : {"X-CSRFToken":$.cookie("csrftoken")},
		})
		.done(function(data) {
			$(".makeStyles-active-328").find('.txt_last_msg').text(data.content);
			message = data.content;
			if(data.file!=null){
				message = `<b><a href="${data.file}">${data.content}</a></b>`;
			}
			socket.send(
				JSON.stringify({
					"source":data.source,
					"destination":data.destination,
					"id":data.id,
					"message":message,
					"timestamp":data.timestamp,
					"type":"chat_message"
				})
			);
			my_avatar = $('#my_avatar').attr('src');
			$("#messages_boddy").append(templMyMsg(data.id, message, data.timestamp));
			$form.trigger("reset");
			div = $("#messages_boddy").parent(".bd-content");
			div.scrollTop(div.prop("scrollHeight"));
		})
		.fail(function() {
			console.log("failed")
		})
		.always(function() {
			console.log("complete");
		});
	});//on submit
	$(".bd-content").on('click', '.deleteMessage', function(event) {
		console.log("Clicked deletion");
		event.preventDefault();
		id_message = $(event.currentTarget).attr('data-id');
		socket.send(
			JSON.stringify({
				"message":id_message,
				"type":"deletion"
			})
		);
	});
};//socket
scrollDown();

$('#search_email').keyup(function(event) {
	for(let label of $(".message_content")){
		content = $(label).text().trim();
		if(content.toLowerCase().includes($(this).val().toLowerCase())){
			$(label).css("display","flex");
		}else{
			$(label).css("display","none");
		}
	}
});

$('#contact-search').keyup(function(event) {
	for(let label of $(".contact-item")){
		content = $(label).find(".font-weight-bold").text().trim();
		//to search even in lasts messages
		//content = $(label).text().trim();
		if(content.toLowerCase().includes($(this).val().toLowerCase())){
			$(label).css("display","flex");
		}else{
			$(label).css("display","none");
		}
	}
});

});