function captchaBtnClickEvent(event) {
  event.preventDefault();
  var $this = $(this);

  // Obtain the email
  var email = $("input[name='email']").val();
  var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
  if (!email || !reg.test(email)) {
    alert("Please enter the correct format email!");
    return;
  }

  zlajax.get({
    url: "/user/mail/captcha?mail=" + email
  }).done(function (result) {
    alert("Verification code sent successfully!");
  }).fail(function (error) {
    alert(error.message);
  })
}

$(function () {
  $('#captcha-btn').on("click",function(event) {
    event.preventDefault();
    // Obtain the email address
    var email = $("input[name='email']").val();

    zlajax.get({
      url: "/user/mail/captcha?mail=" + email
    }).done(function (result) {
      alert("Verification code sent successfully!");
    }).fail(function (error) {
      alert(error.message);
    })
  });
});