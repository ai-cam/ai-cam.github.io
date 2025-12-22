$(function(){

   $('.loop').on('init', function(e, slick) {
        var $firstAnimatingElements = $('div.item:first-child').find('[data-animation]');
        doAnimations($firstAnimatingElements);
    });
    $('.loop').on('beforeChange', function(e, slick, currentSlide, nextSlide) {
        var $animatingElements = $('div.item[data-slick-index="' + nextSlide + '"]').find('[data-animation]');
        doAnimations($animatingElements);
    });

    $('.home-slider .loop').slick({
        dots: true,
        infinite: true,
        speed: 1000,
        arrows: false,
        autoplay: false,
        autoplaySpeed: 8000,
        fade: true,
        slidesToShow: 1,
        slidesToScroll: 1
    }).on('init', function() {
        reorganizeMobileSlider();
    });
    
    // Home slider arrow controls
    $('.home-slider .slider-arrow-prev').on('click', function() {
        $('.home-slider .loop').slick('slickPrev');
    });
    
    $('.home-slider .slider-arrow-next').on('click', function() {
        $('.home-slider .loop').slick('slickNext');
    });

    // Mobilde dots ve arrow'ları aynı satıra taşı
    function reorganizeMobileSlider() {
        var $sliderWrapper = $('.home-slider .slider-wrapper');
        
        if ($(window).width() <= 992) {
            var $dots = $('.home-slider .slick-dots');
            var $prevArrow = $('.home-slider .slider-arrow-prev');
            var $nextArrow = $('.home-slider .slider-arrow-next');
            
            if ($dots.length && !$sliderWrapper.find('.slider-controls-mobile').length) {
                var $controlsWrapper = $('<div class="slider-controls-mobile"></div>');
                $dots.appendTo($controlsWrapper);
                $prevArrow.appendTo($controlsWrapper);
                $nextArrow.appendTo($controlsWrapper);
                $controlsWrapper.appendTo($sliderWrapper);
            }
        } else {
            var $controlsWrapper = $('.home-slider .slider-controls-mobile');
            if ($controlsWrapper.length) {
                var $dots = $controlsWrapper.find('.slick-dots');
                var $prevArrow = $controlsWrapper.find('.slider-arrow-prev');
                var $nextArrow = $controlsWrapper.find('.slider-arrow-next');
                var $loop = $('.home-slider .loop');
                
                $dots.appendTo($loop);
                $prevArrow.prependTo($sliderWrapper);
                $nextArrow.appendTo($sliderWrapper);
                $controlsWrapper.remove();
            }
        }
    }

    $(window).on('resize', reorganizeMobileSlider);
    reorganizeMobileSlider();
    
    $(".left").on("click",function(){
        $(this).next().slick('slickPrev');
    });
    $(".right").on("click",function(){
        $(this).prev().slick('slickNext');
    });


    $('.find-out-loop').slick({
        dots: true,
        infinite: true,
        speed: 600,
        arrows: false,
        autoplay: false,
        autoplaySpeed: 5000,
        fade: false,
        slidesToShow: 3,
        slidesToScroll: 3,
        responsive: [
    {
      breakpoint: 992,
      settings: {
        slidesToShow: 1
      }
    }
  ]
    });

    function doAnimations(elements) {
        var animationEndEvents = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        elements.each(function() {
            var $this = $(this);
            var $animationDelay = $this.data('delay');
            var $animationType = 'animated ' + $this.data('animation');
            $this.css({
                'animation-delay': $animationDelay,
                '-webkit-animation-delay': $animationDelay
            });
            $this.addClass($animationType).one(animationEndEvents, function() {
                $this.removeClass($animationType);
            });
        });
    }
});
