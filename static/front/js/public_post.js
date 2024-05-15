$(function (){
  var editor = new window.wangEditor("#editor");
  editor.config.uploadImgServer  = "/upload/image";
  editor.config.uploadFileName = "image";
  editor.create();
  //alert("editor created")  ;

  // 提交按钮点击事件
  $("#submit-btn").click(function (event) {
      event.preventDefault();
      var title = $("input[name='title']").val();
      var board_id = $("select[name='board_id']").val();
      var content = editor.txt.html();
      var credit = $("input[name='credit']").val();
      //alert("submit-btn click")  ;
      zlajax.post({
        url: "/post/public",
        data: {title,board_id,content,credit}
      }).done(function(data){
          setTimeout(function (){
              window.location = "/";
          },2000);
      }).fail(function(error){
          alert(error.message);
      });
  });

  $("#comment-btn").click(function (event) {
      event.preventDefault();
      var title = $("input[name='title']").val();
      var board_id = $("select[name='board_id']").val();
      var content = editor.txt.html();
      var formid=$("#comment_form");
      var formidaction=$("#comment_form").attr( 'action' );

      //alert("comment-btn click") ;
      zlajax.post({
        url: formidaction,
        data: {title,board_id,content}
      }).done(function(data){
          setTimeout(function (){
              window.location = "/";
          },2000);
      }).fail(function(error){
          alert(error.message);
      });
  });


});