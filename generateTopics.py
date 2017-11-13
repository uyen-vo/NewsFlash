from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from time import time

#http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py 
#The above example was used to write the LDA section of this code.

import numpy
import scipy
import json

dataset_name = "json_test.json"

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

 
#----------------------------------------------------------Lda---------------------------------------------------------

#This was given in the example. It will be replaced with a function that ouputs all topics to a JSON file.
def print_top_words(model, feature_names, n_top_words):
    with open("Generated_Topics.txt", 'w') as f:
        for topic_idx, topic in enumerate(model.components_):
            message = "Topic #%d: " % topic_idx
            message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])

            #Output to a file
            f.write(message + "\n")
            #print(message)
    #print()


data_size = 8000    #How many of the total data set will be used
n_features = 1000
n_components = 50
max_iterations = 10
n_top_words = 20

print("Data size set to: %i" % data_size)
print("Number of Features set to: %i" % n_features)
print("Number of Components set to: %i" % n_components)
print("Max Number of Iterations set to: %i\n" % max_iterations)

corpus = []   #Title & Document
print("Generating set of terms...")
t = time()

#Data set to run LDA
for j in json_list[:data_size]:
    corpus.append(j['title'])
    corpus.append(j['text'])

print("Elapsed Time: %0.3fs \n" % (time() - t))

#TF and TFIDF functions
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words='english')
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words='english')

print("Computing title & document TF & TFIDF...")
t = time()

#Compute TF and TFIDF
tf = tf_vectorizer.fit_transform(corpus)
tfidf = tfidf_vectorizer.fit_transform(corpus)

print("Elapsed Time: %0.3fs \n" % (time() - t))

#LDA function
tf_lda = LatentDirichletAllocation(n_components=n_components, max_iter=max_iterations, learning_method='online', learning_offset=50., random_state=0)
tfidf_lda = LatentDirichletAllocation(n_components=n_components, max_iter=max_iterations, learning_method='online', learning_offset=50., random_state=0)

print("Computing LDA...")
t = time()

#Compute LDA
tf_lda.fit(tf)
#tfidf_lda.fit(tfidf)

print("Elapsed Time: %0.3fs." % (time() - t))

#Get the topics generated
tf_features = tf_vectorizer.get_feature_names()
#tfidf_features = tfidf_vectorizer.get_feature_names()

#Print results
print("\nTopics in TF LDA model:")
print_top_words(tf_lda, tf_features, n_top_words)

print("\nTopics in TFIDF LDA model:")
#print_top_words(tfidf_lda, tfidf_features, n_top_words)

