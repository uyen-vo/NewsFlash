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
	$( ".img-output" ).fadeTo(3, 1);

	$text = $('textarea#input').val();
	$result = ""
	$.getJSON('/get_images', {
			a: $('textarea#input').val()
		  }, function(data) {
			console.log(data)
			result = data
			getImages(result[0], "one");
			getImages(result[1], "two");
			getImages(result[2], "three");

			// TODO: case for less than 3 topics
		  });
}

function getImages( term, divNum ) {
	var URL = "https://pixabay.com/api/?key="+API_KEY+"&q="+encodeURIComponent(term);
	$.getJSON(URL, function(data){
	if (parseInt(data.totalHits) > 0){
		console.log(parseInt(data.totalHits))
		$( "." + divNum ).empty();
		$( "." + divNum + "-container p" ).empty();

		var title = "Images related to <i><b>" + term + "</b></i>";
		$( "." + divNum + "-container p" ).append( title );

		$.each(data.hits, function(i, hit) {
			var imgClass = ''
			if ( hit.webformatHeight > hit.webformatWidth ) {
				imgClass = 'fillwidth';
			} else {
				imgClass = 'fillheight';
			}

			var caption = "<a href='" + hit.pageURL + "'>Click here for a free full-scale download of this high-res image.</a>";
			
			var newDiv = "<div class='o-item'><a href='" + hit.webformatURL +"' data-lightbox='" + term + "' data-title='<a href=\"" + hit.pageURL + "\">Click here</a> to download full-scale high-res image.'><img class='" + imgClass + "' src='" + hit.webformatURL + "'/></a></div>";
			$( "." + divNum ).append( newDiv );
		});
	}
	else {
		// TODO: case for no hits returned -> check out next topic(s)
		console.log('No hits');
	}
	});
}