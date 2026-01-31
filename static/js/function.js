console.log("review js loaded");

// ⭐ STAR CLICK
$(document).on("click", ".rating-stars .star", function () {

    let value = $(this).data("value");

    $("#id_rating").val(value);

    $(".rating-stars .star").removeClass("active");
    $(".rating-stars .star").each(function () {
        if ($(this).data("value") <= value) {
            $(this).addClass("active");
        }
    });

    console.log("STAR SELECTED:", value);
});


// 📝 FORM SUBMIT
$(document).on("submit", "#commentForm", function (e) {
    e.preventDefault();

    let rating = $("#id_rating").val();
    if (!rating) {
        alert("Please select a rating ⭐");
        return;
    }

    let form = $(this);

    $.ajax({
        url: form.attr("action"),
        method: "POST",
        data: form.serialize(),
        dataType: "json",

        success: function (response) {
            console.log("AJAX RESPONSE:", response);

            if (response.bool === true) {

                // ✅ Hide textarea + button
                $("#review-form-area").hide();

                // ✅ Show success / update message
                if (response.created === true) {
                    $("#review-success")
                        .text("✅ Thank you for your review!")
                        .fadeIn(300);
                } else {
                    $("#review-success")
                        .text("✏ Your review has been updated")
                        .fadeIn(300);
                }

                // ✅ Safely append review (ONLY if list exists)
                if ($(".comment-list").length) {
                    let stars = "";
                    for (let i = 0; i < response.context.rating; i++) {
                        stars += '<i class="fa fa-star text-warning"></i>';
                    }

                    $(".comment-list").prepend(`
                        <div class="reply-comment-item">
                            <strong>${response.context.user}</strong>
                            <div>${stars}</div>
                            <p>${response.context.review}</p>
                            <small>${response.context.date}</small>
                        </div>
                    `);
                }
            }
        },

        error: function (xhr) {
            console.error("AJAX ERROR:", xhr.responseText);
            alert("Something went wrong. Please refresh.");
        }
    });
});





//current-product-price

// Add to cart functionality




$(".btn-add-to-cart").on('click', function(){
    let this_val = $(this);
    let index = this_val.attr('data-index');
    let selected_image = $(".main-product-image").attr("src");

    let quantity =$(".product-quantity-" + index).val();
    let product_title =$(".product-title-" + index).val();
    let product_id =$(".product-id-" + index).val();
    let product_price =$(".current-product-price-" + index).val();
    let product_pid =$(".product-pid-" + index).val();
    
    let product_size =$(".product-size-" + index + " option:selected").val()
    let product_color = $(".product-color-" + index).val()

    



    if (!product_size) {
    product_size = "40";   // You can write "Free Size" or first size
}

   if (!product_color) {
    let firstSwatch = $(".swatch").first();

    product_color = firstSwatch.data("color");
    selected_image = firstSwatch.data("image");}

   if (!selected_image) {
    selected_image = $(".main-product-image").attr("src");
}

    console.log('Quantity:',quantity);
    console.log('Title:',product_title);
    console.log('ID:',product_id);
    console.log('Pid:',product_pid);
   
    console.log('Price:',product_price);
    console.log('Index:',index);
    console.log('Current element:',this_val);
    console.log('Size:',product_size);
    console.log('Color:',product_color);
    console.log('Selected Image:',selected_image);

    $.ajax({

        url: '/add-to-cart/',
        data: {
            'id': product_id,
            'pid': product_pid,
            'image': selected_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
            'size': product_size,
            'color': product_color,
            

            
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Adding product to cart..');
            
        
        },
        success: function(response){
            this_val.html('Item Added to Cart');
            console.log('Added product to cart...');
            $(".cart-items-count").text(response.totalcartsitems);
        }
    })


})

// COLOR SWATCH CLICK (FINAL)
$(document).on("click", ".swatch", function () {

    let color = $(this).data("color");
    let image = $(this).data("image");
    let product_id = $(this).data("product");

    console.log("Swatch clicked: ", color, image, product_id);

    // Hidden color update
    $(".product-color-" + product_id).val(color);
    $(".product-image-" + product_id).val(image);

    // Main image update
    $(".main-product-image").attr("src", image);
    $(".main-product-image").attr("data-src", image);
    $(".main-product-image").attr("data-zoom", image);

     console.log("Saved Color:", color);
    console.log("Saved Image:", image);

    // UI me active class
    $(".swatch[data-product='" + product_id + "']").removeClass("active");
    $(this).addClass("active");
});





$(".delete-product").on('click', function(){
    
    let product_id = $(this).attr('data-product');
    let this_val =$(this) 
    console.log("Product ID",product_id);

    $.ajax({
        url: '/delete-from-cart',
        data: {
            'id': product_id,
        },
        dataType: 'json',
        beforeSend: function(){
            this_val.hide();
        },
        success: function(response){
            this_val.show();
            $(".cart-items-count").text(response.totalcartsitems);
            $("#cart-list").html(response.data);
            
        }
})
})


$(document).ready(function() {
        $('.color-btn').click(function () {
            let newImage = $(this).data('image'); 

            // Main image change
            $('.main-product-image').attr('src', newImage);
            $('.main-product-image').attr('data-src', newImage);

            // Zoom image tab change (optional)
            $('.tf-image-zoom').attr('data-zoom', newImage);
     });
 });


         //  buy now checkout 

$(document).on("click", ".btn-buy-now", function (e) {
    e.preventDefault();
    console.log("BUY NOW CLICKED");


    let index = $(this).data("index");

    let product_title = $(".product-title-" + index).val();
    let product_id = $(".product-id-" + index).val();
    let product_pid = $(".product-pid-" + index).val();
    let product_price = $(".current-product-price-" + index).val();
    let product_size = $(".product-size-" + index).val();
    let product_color = $(".product-color-" + index).val();
    let selected_image = $(".main-product-image").attr("src");
    let quantity =$(".product-quantity-" + index).val();

    // Safety fallback
    if (!product_size) product_size = "Free Size";
    if (!product_color) product_color = "Default";

    $.ajax({
        url: "/buy-now/",
        method: "POST",
        data: {
            id: product_id,
            pid: product_pid,
            title: product_title,
            price: product_price,
            size: product_size,
            color: product_color,
            image: selected_image,
            qty: quantity,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function (response) {
            if (response.status === "success") {
                window.location.href = "/checkout/";
            }
        }
    });
});

 
$(document).on("click", ".make-default-address", function(){
    let id = $(this).attr("data-address-id");
    let this_val = $(this);
    
    console.log("Address ID:",id);
    console.log("Current element:",this_val);

    $.ajax({
        url: '/make-default-address/',
        data: {
            'id': id,
        },
        dataType: 'json',
        success: function(response){
            console.log('Made default address...');
            if (response.boolean == true){
                $(".check").hide();
                $(".action_btn").show();

                $(".check" + id).show();
                $(".button" + id).hide();
            }
        }
    })

});


$(document).on("submit", "#contact-form-ajax", function(e){
    e.preventDefault();
    console.log("Contact form submitted");

    let full_name = $("#full_name").val();
    let email = $("#email").val();
    let phone = $("#phone").val();
    let subject = $("#subject").val();
    let message = $("#message").val();
    console.log("Name:", full_name);
    console.log("Email:", email);
    console.log("Phone:", phone);
    console.log("Subject:", subject);
    console.log("Message:", message);

    $.ajax({
        url: '/ajax-contact-form',
        data:{
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'message': message,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Sending data to server...');
        },
        success: function(response){  
            console.log('Data sent to server successfully.');
            $("#contact-form-ajax").hide();
            $("#message-response").html("Message sent successfully!");
        }
        })
});



