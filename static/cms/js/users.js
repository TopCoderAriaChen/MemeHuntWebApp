$(function (){
  $(".active-btn").click(function (event){
    event.preventDefault();
    var $this = $(this);
    var is_active = parseInt($this.attr("data-active"));
    var message = is_active?"Are you sure you want to disable this user？":"Are you sure you want to unban this user？";
    var user_id = $this.attr("data-user-id");
    var result = confirm(message);
    if(!result){
      return;
    }
    var data = {
      is_active: is_active?0:1
    }
    console.log(data);
    zlajax.post({
      url: "/cms/users/active/" + user_id,
      data: data
    }).done(function (){
      window.location.reload();
    }).fail(function (error){
      alert(error.message);
    })
  });
});