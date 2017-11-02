var http = require('http'),
	fs = require('fs'),
	async = require('async'),
	express = require('express'),
	jsonfile = require('jsonfile');


var documents = {};
var dictionary = {};
	


http.createServer(function (request, response) {
   response.writeHead(200, {'Content-Type': 'text/plain'});
   response.end('Hello World\n');
}).listen(8081);

// Console will print the message
console.log('Server running at http://127.0.0.1:8081/');


initialize();

function initialize() {
	var numCalls = 80000;
	var zeroes = '000000';
	for(var i = 1; i<=80000; i++) {
		if (i == 10 || i == 100 || i == 1000 || i == 10000 || i == 100000){
			zeroes = zeroes.substring(0, zeroes.length - 1);
		}

		var url = 'full-sample/news_' + zeroes + i + '.json';
		
		jsonfile.readFile(url, function(err, obj) {
			addDocObj(obj);
			numCalls--;
				
			if (numCalls == 0) {
				outputStats();
			}
		})
	}
}

/* Constructs a single document object and adds it to the documents */
function addDocObj(obj) {
    var out = "";
	var titleC
	var docObj = {};
	var wordCount = {};
	var wordArray = obj.text.split(" ");
	var maxWord = '';
	var maxCount = 0;
	
	for(var i = 0; i < wordArray.length; i++) {
		var word = wordArray[i];
		wordCount[word] = wordCount[word] ? wordCount[word] + 1 : 1;
		
		if (wordCount[word] > maxCount) {
			maxWord = word;
			maxCount = wordCount[word];
		}
	}
	
	docObj['word_count'] = wordCount;
	docObj['char_count'] = obj.text.length; // Handle: establish a minimum char counts (spam filter)
	docObj['title_count'] = obj.title.length; // Handle: title_count == 0
	docObj['max_word'] = maxWord;
	docObj['max_count'] = maxCount;
	
	documents[obj.uuid] = docObj;
}

/* Checkpoint 1: output document statistics */
function outputStats(){
	console.log('*******Outputting stats*******');
	var avgDocLength, avgTitleLength = 0;
	
	var totalDocLength = 0;
	var totalTitleLength = 0;
	var numDocs = Object.keys(documents).length;
	
	for (var key in documents) {
		if (documents.hasOwnProperty(key)) {   
			//console.log(key, documents[key]);        
			totalDocLength += documents[key].char_count;
			totalTitleLength += documents[key].title_count;
			
			
			for (var k in documents[key].word_count) {
				if (dictionary[k]) {
					dictionary[k].doc_freq += 1;
				} else {
					var dictObj = new Object();
					dictObj.doc_freq = 1;
					dictionary[k] = dictObj;
				}
			}
		}
	}
	
	avgDocLength = totalDocLength / Object.keys(documents).length;;
	avgTitleLength = totalTitleLength / numDocs;

	var topFive = Object.keys(dictionary).map(function(key) {
		return [key, dictionary[key].doc_freq];
	});

	topFive.sort(function(first, second) {
		return second[1] - first[1];
	});
	console.log('Average doc length (characters): ' + avgDocLength);
	console.log('Average title length (characters): ' + avgTitleLength);
	console.log('Top 5 document frequencies: ');
	for (var i = 0; i < 4; i++) {
		console.log('>' + (i+1) + '. ' + topFive.slice(0, 5)[i][0] + ' ' + topFive.slice(0, 5)[i][1]);
	}
}