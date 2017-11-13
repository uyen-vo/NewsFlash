General
- json80K.json contains our 80,000 documents
- generateTopics.py reads in json80K.json and groups the words across all documents into N topics
- currently writes to a .txt file but we will have it output in JSON format as input for our JS code (client/server)
- run via:
	python generateTopics.py
	with json80K.json in the same directory

Dependencies
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from time import time
import numpy
import scipy
import json