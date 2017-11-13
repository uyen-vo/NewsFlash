// GENERAL
- json_test.json.zip contains json_test.json, our test set (10,000 documents)
- generateTopics.py reads in json_test.json and groups the words across all documents into N topics (50 currently)
- currently writes to a Generated_Topics.txt file but we will soon have it output in JSON format as input for our JS code (client/server)
- we have implemented the LDA in python and client-side TF/DF in JavaScript as our core algorithms but have yet to link the two
- run via:
	python generateTopics.py
	with json_test.json in the same directory


// DEPENDENCIES
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from time import time
import numpy
import scipy
import json