
// 'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Gallery filter
        --------------------*/
        $('.featured__controls li').on('click', function () {
            $('.featured__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.featured__filter').length > 0) {
            var containerEl = document.querySelector('.featured__filter');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Humberger Menu
    $(".humberger__open").on('click', function () {
        $(".humberger__menu__wrapper").addClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").addClass("active");
        $("body").addClass("over_hid");
    });

    $(".humberger__menu__overlay").on('click', function () {
        $(".humberger__menu__wrapper").removeClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").removeClass("active");
        $("body").removeClass("over_hid");
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*-----------------------
        Categories Slider
    ------------------------*/
    $(".categories__slider").owlCarousel({
        loop: false,
        margin: 0,
        items: 7,
        dots: false,
        // navigation : true,
        navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1000,
        autoHeight: false,
        autoplay: true,

    });

    $(".banner").owlCarousel({
        loop:true,
        margin:0,
        responsiveClass:true,
        dots: true,
        smartSpeed: 1200,
        autoHeight: true,
        autoplay: true,
        responsive:{
            0:{
                items:1,
                nav:true
            },
            600:{
                items:1,
                nav:false
            },
            1000:{
                items:1,
                nav:true,
                loop:false
            }
        }

    });


    /*-----------------------------
        Product Discount Slider
    -------------------------------*/

    $('.product__discount__slider').owlCarousel({
        loop:true,
        margin:0,
        responsiveClass:true,
        dots: true,
        smartSpeed: 1200,
        autoHeight: true,
        autoplay: true,
        responsive:{
            0:{
                items:2,
                nav:true
            },
            600:{
                items:4,
                nav:false
            },
            1000:{
                items:6,
                nav:true,
                loop:false
            }
        }
    })



    $(".product_shop_slider").owlCarousel({
        loop:true,
        margin:0,
        responsiveClass:true,
        dots: true,
        smartSpeed: 1200,
        autoHeight: true,
        autoplay: true,
        responsive:{
            0:{
                items:2,
                nav:true
            },
            600:{
                items:4,
                nav:false
            },
            1000:{
                items:6,
                nav:true,
                loop:false
            }
        }
    });


    /*---------------------------------
        Product Details Pic Slider
    ----------------------------------*/
    $(".product__details__pic__slider").owlCarousel({
        loop:true,
        margin:0,
        responsiveClass:true,
        dots: true,
        smartSpeed: 1200,
        autoHeight: true,
        autoplay: true,
        responsive:{
            0:{
                items:2,
                nav:true
            },
            600:{
                items:4,
                nav:false
            },
            1000:{
                items:6,
                nav:true,
                loop:false
            }
        }

    });

    /*-----------------------
		Price Range Slider
	------------------------ */
    var rangeSlider = $(".price-range"),
        minamount = $("#minamount"),
        maxamount = $("#maxamount"),
        minPrice = rangeSlider.data('min'),
        maxPrice = rangeSlider.data('max');
    rangeSlider.slider({
        range: true,
        min: minPrice,
        max: maxPrice,
        values: [minPrice, maxPrice],
        slide: function (event, ui) {
            minamount.val('$' + ui.values[0]);
            maxamount.val('$' + ui.values[1]);
        }
    });
    minamount.val('$' + rangeSlider.slider("values", 0));
    maxamount.val('$' + rangeSlider.slider("values", 1));

    /*--------------------------
        Select
    ----------------------------*/
    // $("select").niceSelect();

    /*------------------
		Single Product
	--------------------*/
    $('.product__details__pic__slider img').on('click', function () {

        var imgurl = $(this).data('imgbigurl');
        var bigImg = $('.product__details__pic__item--large').attr('src');
        if (imgurl != bigImg) {
            $('.product__details__pic__item--large').attr({
                src: imgurl
            });
        }
    });

    /*-------------------
		Quantity change
	--------------------- */
    var proQty = $('.pro-qty');
    proQty.prepend('<span class="dec qtybtn">-</span>');
    proQty.append('<span class="inc qtybtn">+</span>');
    proQty.on('click', '.qtybtn', function () {
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        $button.parent().find('input').val(newVal);
    });

})(jQuery);




$(document).ready(function(){

    // $ ("#varticalmanu").menu();

    $('#id_price_0').attr('class', 'text-muted');
    $('#id_price_0').attr('placeholder', 'Minimum Price');
    
    $('#id_price_1').attr('placeholder', 'Maximum Price');
    $('#id_price_1').attr('class', 'text-muted');
  

});


$('.hero__categories__all').on('click', function(){
    $('.hero__categories ul').slideToggle(400);
});



// hit shop/shop-grid.html
// $('#id_colors').on('input', function() { 
//     $('#color_search_btn').trigger('click');
// });



$('#id_colors_1').on('input', function() { 
    $('#color_search_btn').trigger('click');
});

$('#id_colors_2').on('input', function() { 
    $('#color_search_btn').trigger('click');
});

$('#id_colors_3').on('input', function() { 
    $('#color_search_btn').trigger('click');
});

$('#id_colors_4').on('input', function() { 
    $('#color_search_btn').trigger('click');
});

$('#id_colors_5').on('input', function() { 
    $('#color_search_btn').trigger('click');
});

$('#id_colors_5').on('input', function() { 
    $('#color_search_btn').trigger('click');
});

$('#id_colors_6').on('input', function() { 
    $('#color_search_btn').trigger('click');
});
$('#id_colors_7').on('input', function() { 
    $('#color_search_btn').trigger('click');
});



$(".banner").owlCarousel({
    // loop: true,
    margin: 0,
    items: 1,
    dots: false,
    nav: true,
    navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
    animateOut: 'fadeOut',
    animateIn: 'fadeIn',
    smartSpeed: 500,
    autoHeight: false,
    autoplay: true,

});


