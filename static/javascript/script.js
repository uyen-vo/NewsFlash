var about = false;
var dev = false;
var API_KEY = '6980968-e13a5874e345e16b4a8c7f66a';


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
	$result = ""
	$.getJSON('/get_images', {
			a: $('textarea#input').val()
		  }, function(data) {
			console.log(data)
			result = data
			var URL = "https://pixabay.com/api/?key="+API_KEY+"&q="+encodeURIComponent(result[0]);
			$.getJSON(URL, function(data){
			if (parseInt(data.totalHits) > 0)
				//$.each(data.hits, function(i, hit){ console.log(hit.webformatURL); });
				$.each(data.hits, function(i, hit) {
					var imgClass = ''
					if ( hit.webformatHeight > hit.webformatWidth ) {
						imgClass = 'fillwidth';
					} else {
						imgClass = 'fillheight';
					}
					
					var newDiv = "<div class='o-item'><img class='" + imgClass + "' src='" + hit.webformatURL + "'/></div>";
					$( ".img-output" ).append( newDiv );
					console.log(newDiv)
				});
			else
				console.log('No hits');
			});
		  });
}