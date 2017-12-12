from flask import Flask, jsonify, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from operator import itemgetter
import numpy
import scipy
import json
import jinja2
import urllib

app = Flask(__name__, static_folder='static')
app.jinja_loader = jinja2.FileSystemLoader('.')

#This pyhton script
# 1) Takes in the text of the new document 
# 2) Runs LDA on the text
# 3) Compares the list of topics to our database of topics. This is done to get more topics related to the new document. OPTIONAL
# 4) Sends the list of topics to the image API
# 5) Sends the list of urls from the image API back to our webpage 
# 6) The webpage displays the list of image urls


#----------------------------------------------------------------------------------------------------------------------

def output_to_file(file_name, doc_list):
    with open(file_name, 'w') as f:
        for doc in doc_list:
            f.write(doc + '\n')

def getTopicJson(json_obj, obj_index, model, feature_names, top_n):
    r_json = ""
    tags = {}
    for topic_idx, topic in enumerate(model.components_):   #Generate JSON
        for i in (-topic).argsort()[:top_n]:
            tags.update( { feature_names[i] : (topic[i] / float(len(-topic))) } )

        output_json = { 'index' : obj_index, 'tags' : sorted(tags.items(), key=itemgetter(1), reverse=True) } 

        r_json += json.dumps( output_json, sort_keys=True, separators=(', ', ': ') ) 
    return r_json
 
def getTopicNewDoc(obj_index, model, feature_names, top_n):
    r_json = ""
    tags = {}
    for topic_idx, topic in enumerate(model.components_):   #Generate JSON
        for i in (-topic).argsort()[:top_n]:
            tags.update( { feature_names[i] : (topic[i] / float(len(-topic))) } )

        output_json = { 'index' : obj_index, 'tags' : sorted(tags.items(), key=itemgetter(1), reverse=True) } 

        r_json += json.dumps( output_json, sort_keys=True, separators=(', ', ': ') ) 
    return r_json
	
def get_topics(model, feature_names, top_n):
	tags = []
	for topic_idx, topic in enumerate(model.components_):
		tags = [feature_names[i] for i in (-topic).argsort()][:top_n]
	return tags
	
@app.route('/get_images')
def get_images():
	a = urllib.unquote(request.args.get('a', "", type=str))
	b = urllib.unquote(request.args.get('b', "", type=str))
	
	doc_text = a
	for i in range(0,6):
		doc_text += " " + b
	print doc_text
	doc_topics = {}
	#-------------------------------------------Setup LDA-------------------------------------------
	n_features = 1000   #Number of most frequent words used to build vocabulary
	n_components = 1
	max_iterations = 5
	n_top_words = 20

	topics = []
	topic_index = 0

	corpus = []
	corpus.append(doc_text)

	#TF and TFIDF functions
	tf_vectorizer = CountVectorizer(max_df=1.0, min_df=1, max_features=n_features, stop_words='english')

	#LDA function
	tf_lda = LatentDirichletAllocation(n_components=n_components, max_iter=max_iterations, learning_method='online', learning_offset=20., random_state=0)

	#------------------------------------------Run LDA------------------------------------------

	#Run LDA on doc
	tf_lda.fit(tf_vectorizer.fit_transform(corpus))

	#------------------------------------------Topic Results------------------------------------------
	doc_topics = get_topics(tf_lda, tf_vectorizer.get_feature_names(), n_top_words)
	return jsonify(doc_topics)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
