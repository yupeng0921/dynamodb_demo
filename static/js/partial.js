$("#btnId").click(function(){
		$.ajax({
			url: "/", type: "POST",
					data: $('#divCustomerInfo :text').fieldSerialize(),
					success: function(responseText){
					alert(responseText);
				}
			});
		return false;
	});
