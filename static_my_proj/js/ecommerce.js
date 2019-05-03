$(document).ready(function(){
	// Contact Form Handler
	var contactForm = $(".contact-form")
	var contactFormMethod = contactForm.attr("method")
	var contactFormEndpoint = contactForm.attr("action")
	


	function displaySubmitting(submitBtn,defaultText,doSubmit){
		if(doSubmit){
			submitBtn.addClass("disabled")
			submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending ...")
		}else {
			submitBtn.removeClass("disabled")
			submitBtn.html(defaultText)
		}
	}

	contactForm.submit(function(event){

		event.preventDefault()
		var contactFormSubmitBtn = contactForm.find("[type='submit']")
		var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
		var contactFormData = contactForm.serialize()
		var thisForm = $(this)
		displaySubmitting( contactFormSubmitBtn,"",true)
		$.ajax({
			method: contactFormMethod,
			url: contactFormEndpoint,
			data: contactFormData,
			success: function(data){
				contactForm[0].reset()
				$.alert({
					title: "Success!",
					content: data.message,
					theme:"modern"
				})
				setTimeout(function(){
					displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
				},500)
			},
			error: function(error){
				var jsonData = error.responseJSON
				var msg = ""
				$.each(jsonData,function(key,value){
					msg += key +": "+value[0].message +"<br/>"
				})
				$.alert({
					title: "Oops!",
					content: msg,
					theme:"modern",
				})
				setTimeout(function(){
					displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
				},500)
			}
		})
	})



	// Products removing ad adding
	var productForm = $(".form-product-ajax")


	productForm.submit(function(event){
		event.preventDefault();
		var thisForm = $(this)
		var actionEndpoint = thisForm.attr("data-endpoint");
		var httpMethod = thisForm.attr("method");
		var formData = thisForm.serialize();

		$.ajax({
			url: actionEndpoint,
			method: httpMethod,
			data: formData,
			success: function(data){
				var submitSpan = thisForm.find(".submit-span")
				if(data.added){
					submitSpan.html("In cart <button id='remove' type='submit' class='remove btn btn-link'>Remove</button>")

				} else{
					submitSpan.html("<button id='add' type='submit' class='add btn btn-success'>Add to cart</button>")
				}
				var navbarCount	= $(".header-icons-noti")
				navbarCount.text(data.cartItemCount)
				var currentPath = window.location.href
				if(currentPath.indexOf("cart") != -1){
					refreshCart()
				}
				//refreshCart()			
				console.log(data)	
			},
			error: function(errorData){
				$.alert({
					title: "Oops!",
					content: "An error occurred",
					theme:"modern"
				})
			}
		})
	})

	function refreshCart(){
		var cartTable = $(".cart-table")
		var cartBody = cartTable.find(".cart-body")
		//cartBody.html("<h1>Changed</h1>")
		var productRows = cartBody.find(".cart-product")
		var currentUrl = window.location.href

		var refreshCartUrl = '/api/cart/'
		var refreshCartMethod = "GET";
		var data= {};
		$.ajax({
			url: refreshCartUrl,
			method: refreshCartMethod,
			data: data,
			success: function(data){
				console.log(data)
				var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
				if(data.products.length > 0)
				{
					productRows.html(" ")
					i = data.products.length
					$.each(data.products, function(index,value){
						var newCartItemRemove = hiddenCartItemRemoveForm.clone()
						newCartItemRemove.css("display","block")
						newCartItemRemove.find(".cart-item-product-id").val(value.id)
						cartBody.prepend("<tr><th scope=\"row\">"+ i +"</th><td><img src='"+value.image+"' height='100' width='100'></td><td><a href='"+ value.url +"'>" + value.name + "</a>" + newCartItemRemove.html()+ "</td><td>"+ value.price+"</td></tr>")
						i --
					})

					cartBody.find(".cart-subtotal").text(data.subtotal)
					cartBody.find(".cart-total").text(data.total)
				}else{
					window.location.href = currentUrl
				}
			},
			error: function(errorData){
				$.alert({
					title: "Oops!",
					content: "An error occurred",
					theme:"modern"
				})
			}
		})
	}
})