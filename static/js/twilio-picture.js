debug = ''
$(document).ready(function() {
  $('#closemodal').click(function(){
    $('#myModal').modal('hide'); 
  });
  
  // Grab elements, create settings, etc.
  var canvas = $("#canvas")[0]
  context = canvas.getContext("2d")
  video = $("#video")[0]
  videoObj = { "video": true }
  errBack = function(error) {
    console.log("Video capture error: ", error.code); 
  };

  // Put video listeners into place
  if(navigator.getUserMedia) { // Standard
    navigator.getUserMedia(videoObj, function(stream) {
      video.src = stream;
      video.play();
    }, errBack);
  } 
  else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
    navigator.webkitGetUserMedia(videoObj, function(stream){
      video.src = window.webkitURL.createObjectURL(stream);
      video.play();
    }, errBack);
  }

  $("#snap").click(function() {
    context.drawImage(video, 0, 0, 640, 480);
  }); 

  $('#myModal').modal();
  $('#error-name, #error-phone').hide();
  $("#twipic-play").click(function(){
    console.log('here');
    if($('#twipic-name').val().trim() == ''){
      $('#error-name').show();
      return;
    }
    $.post( "/text", {name:$('#twipic-name').val(),phone:$('#twipic-phone').val()},function( data ) {
      $('#myModal').modal('hide');
      console.log("data after success: "+data+ " and phone: "+data.phone);
      $('#twipic-hphone').val(data.phone)
    });
  });
 
  $('#twipic-send').click( function(){
    myImage = canvas.toDataURL('image/png');     
    $.post('/send',{base64img:myImage,phone:$('#twipic-hphone').val(),code:$('#twipic-code').val()});
  }); 
  
  
});


