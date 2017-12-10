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
			a: $('textarea#input').val(),
			b: $('textarea#title').val()
		  }, function(data) {
			console.log(data)
			result = data
			getImages(result)

			// TODO: case for less than 3 topics
		  });
}

function getImages( result ) {
	topicsFound = 0
	var i = 0;
	divNum = ["one", "two", "three", "four", "five"];
	console.log("results length: " + result.length);
	while(topicsFound < 5 && i < result.length)
	{
		console.log(i)
		term = result[i]
		console.log("term" + term);
		var URL = "https://pixabay.com/api/?key="+API_KEY+"&per_page=18&response_group=high_resolution&q="+encodeURIComponent(term);
		$.ajax({
			dataType: "json",
			url: URL,	
			async: false,
			success: function(data) {
				console.log(parseInt(data.totalHits));
				if (parseInt(data.totalHits) > 0){
					++topicsFound
					$( "." + divNum[topicsFound] ).fadeTo(3, 1);
					$( "." + divNum[topicsFound] ).empty();
					$( "." + divNum[topicsFound] + "-container p" ).empty();
					$( "." + divNum[topicsFound] + "-container").css("display", "block");

					num = ''
					switch (divNum[topicsFound - 1]) {
						case 'one' : num = 1; break;
						case 'two' : num = 2; break;
						case 'three' : num = 3; break;
						case 'four' : num = 4; break;
						case 'five' : num = 5; break;
					}
					console.log("TERM BEFORE TITLE: " + term)
					var title = "<b>Topic " + num + ": <i>" + term + "</i></b>";
					$( "." + divNum[topicsFound] + "-container p" ).append( title );

					console.log(data.hits)

					$.each(data.hits, function(i, hit) {
						var imgClass = ''
						if ( hit.webformatHeight > hit.webformatWidth ) {
							imgClass = 'fillwidth';
						} else {
							imgClass = 'fillheight';
						}
						
						var newDiv = "<div class='o-item'><a href='" + hit.webformatURL +"' data-lightbox='" + term + "' data-title='<a href=\"" + hit.fullHDURL + "\" download>Click here</a> to download full-scale high-res image.'><img class='" + imgClass + "' src='" + hit.webformatURL + "'/></a></div>";
						$( "." + divNum[topicsFound] ).append( newDiv );
					});
				}
				else {
					// TODO: case for no hits returned -> check out next topic(s)
					console.log('No hits' + divNum[topicsFound] + " " + term);
				}
		}
		
	});
	i++
	// TODO: show more &page=2, &per_page=N
	}
}