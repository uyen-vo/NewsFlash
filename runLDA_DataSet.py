from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from time import time

#http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py 

import numpy
import scipy
import json
import sys

dataset_name = "DataSet/jsonDataSet.json"
#dataset_name = "DataSet/json_test.json"

json_obj = open(dataset_name, 'r')

json_list = []

#----------------------------------------------------------------------------------------------------------------------
print("\nExtracting data from datset: %s ..." % dataset_name)
t = time()

#Add each json from all the files to json_list
for j_obj in json_obj:
    json_list.append(json.loads(j_obj))

print("Elapsed Time: %0.3fs \n" % (time() - t))




#----------------------------------------------------------------------------------------------------------------------

def output_to_json(file_name, model, feature_names, top_n):
    with open(file_name, 'w') as f:
        for topic_idx, topic in enumerate(model.components_):   #Generate JSON
            output_json = { 'index' : topic_idx, 'tag_list' : [feature_names[i] for i in (-topic).argsort()][:top_n], 'tag_rank' : [topic[i] / float(len(-topic)) for i in (-topic).argsort()][:top_n] } 

            #Output to a file
            f.write(json.dumps( output_json, sort_keys=True, separators=(', ', ': ') ) + '\n')


def output_to_file(file_name, doc_list):
    with open(file_name, 'w') as f:
        for doc in doc_list:
            f.write(doc + '\n')

def getTopicJson(json_obj, obj_index, model, feature_names, top_n):
    r_json = ""
    for topic_idx, topic in enumerate(model.components_):   #Generate JSON
        output_json = { 'index' : obj_index, 'tag_list' : [feature_names[i] for i in (-topic).argsort()][:top_n], 'tag_rank' : [topic[i] / float(len(-topic)) for i in (-topic).argsort()][:top_n] } 
        
        r_json += json.dumps( output_json, sort_keys=True, separators=(', ', ': ') ) 
    return r_json
 




#----------------------------------------------------------Lda---------------------------------------------------------

data_size = len(json_list)   #How many of the total data set will be used
n_features = 1000   #Number of most frequent words used to build vocabulary
n_components = 1
max_iterations = 5
n_top_words = 20

topics = []
topic_index = 0
skipped_docs = 0

print("Data size set to: %i" % data_size)
print("Number of Features set to: %i" % n_features)
print("Number of Components set to: %i" % n_components)
print("Max Number of Iterations set to: %i\n" % max_iterations)

#------------------------------------------Setup LDA------------------------------------------

#TF and TFIDF functions
tf_vectorizer = CountVectorizer(max_df=1.0, min_df=1, max_features=n_features, stop_words='english')

#LDA function
tf_lda = LatentDirichletAllocation(n_components=n_components, max_iter=max_iterations, learning_method='online', learning_offset=20., random_state=0)


#-------------------------------------------Run LDA------------------------------------------

print("Running LDA on %i documents..." %data_size)
t = time()

#Run LDA on every doc of DataSet
for j in json_list:
    corpus = []
    
    if j['text'] != "":  #Skip documents that have no text
        text_str = j['title'] + " " + j['text']

        corpus.append(text_str)

        #Run LDA on doc
        tf = tf_vectorizer.fit_transform(corpus)
        tf_lda.fit(tf)

        #Add topics to new dataset
        topics.append(getTopicJson(j, topic_index, tf_lda, tf_vectorizer.get_feature_names(), n_top_words))

        #Print status
        sys.stdout.write('\r')
        sys.stdout.write( str(topic_index + 1) + " out of " + str(data_size) )
        sys.stdout.flush()

        topic_index += 1
    else:
        skipped_docs += 1



print '\n\n'
end_time = (time() - t)
print("Elapsed Time: %0.6fs \n" % (end_time))
print("Average Time: %0.6fs \n" % (end_time / len(json_list)))
print("%i documents skipped \n" % skipped_docs )


#Output topics to file
output_to_file("ldaDataSet.json", topics)