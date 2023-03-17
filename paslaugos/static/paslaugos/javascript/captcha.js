$(document).ready(function() {
  $('.js-captcha-refresh').click(function() {
    $.ajax({
      url: "/refresh_captcha/",
      success: function(data) {
        $('.captcha').html(data);
      }
    });
  });
});