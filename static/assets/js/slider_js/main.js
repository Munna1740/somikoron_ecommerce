$('.home_banner').slick({
  dots: true,
  infinite: true,
  speed: 2000,
  prevArrow:
    '<span class="prev_arrow"><i class="fa fa-chevron-left" aria-hidden="true"></i></span>',
  nextArrow:
    '<span class="next_arrow"><i class="fa fa-chevron-right" aria-hidden="true"></i></span>',
  fade: true,
  autoplay: true,
  cssEase: 'linear',
});

if ($('.slick-slide').hasClass('slick-active')) {
  $('.caption').addClass(' animate__animated animate__bounceInUp');
  $('.animate_add').addClass('animate__animated animate__bounceInUp');
} else {
  $('.caption').removeClass('animated fadeInLeft');
  $('.animate_add').removeClass('animate__animated animate__bounceInUp');
}

$('.home_banner').on('beforeChange', function () {
  $('.caption').removeClass('animate__animated animate__bounceInUp').hide();
  $('.animate_add').removeClass('animate__animated animate__bounceInUp').hide();
  setTimeout(() => {
    $('.caption').addClass('animate__animated animate__bounceInUp').show();
    $('.animate_add').addClass('animate__animated animate__bounceInUp').show();
  }, 1000);
});
