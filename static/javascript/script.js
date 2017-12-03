var about = false;
var dev = false;


function navClick( button ) {
	if (button === 'about') {
		if (!about){
			var height = $( window ).height() - $("nav").height();
			$(".about").height(height);
			$(".left").addClass("active");
			$(".about").animate({left: "0px"}, 500)
			about = true;
		}

		else {
			$(".about").animate({left: "-402px"}, 500)
			$(".left").removeClass("active");
			about = false;
		}
	}

	if (button === 'dev') {
		if (!dev){
			var height = $( window ).height() - $("nav").height();
			$(".dev").height(height);
			$(".dev").animate({right: "0px"}, 500);
			$(".right").addClass("active");
			dev = true;
		}

		else {
			$(".dev").animate({right: "-402px"}, 500);
			$(".right").removeClass("active");
			dev = false;
		}
	}

	if (button === 'main') {
		if (dev) {
			$(".dev").animate({right: "-402px"}, 500);
			$(".right").removeClass("active");
			dev = false;
		}

		if (about) {
			$(".about").animate({left: "-402px"}, 500)
			$(".left").removeClass("active");
			about = false;
		}
	}
	
}

function submitClick() {
	$text = $('textarea#input').val();
/*         $.ajax({
            //the url to send the data to
            url: "/",
            //the data to send to
            data: {text : $text},
			//type. for eg: GET, POST
			type: "POST",
			//datatype expected to get in reply form server
			dataType: "text",
			//on success
            success: function(ret){
                console.log("got" + images);
            },
            //on error
            error: function(){
                console.log(ret);
            }
}); */
/* 	$.getJSON('/get_images', {
        a: $('textarea#input').val()
      }, function(data) {
        console.log(data.result);
	}); */
$.getJSON('/get_images', {
        a: $('textarea#input').val()
      }, function(data) {
        console.log(data.result);
      });
}