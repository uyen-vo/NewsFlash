from time import time
import numpy
import scipy
import json

dataset_name = "DataSet/ldaDataSet.json"

json_obj = open(dataset_name, 'r')
json_list = []

#NOTE: nhl has a lot of repeats

cull_term = "item"      #Docs with 'embed', 'item' have been removed

#----------------------------------------------------------------------------------------------------------------------
print("\nExtracting data from datset: %s ..." % dataset_name)
t = time()

#Add each json from all the files to json_list
for j_obj in json_obj:
    obj = json.loads(j_obj)
    if len(obj['tag_list']) > 2:
        if cull_term not in obj['tag_list']:
            json_list.append(obj)

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
            f.write(json.dumps(doc, sort_keys=True, separators=(', ', ': ') ) + '\n')

def getTopicJson(json_obj, obj_index, model, feature_names, top_n):
    r_json = ""
    for topic_idx, topic in enumerate(model.components_):   #Generate JSON
        output_json = { 'index' : obj_index, 'tag_list' : [feature_names[i] for i in (-topic).argsort()][:top_n], 'tag_rank' : [topic[i] / float(len(-topic)) for i in (-topic).argsort()][:top_n] } 
        
        r_json += json.dumps( output_json, sort_keys=True, separators=(', ', ': ') ) 
    return r_json

 #----------------------------------------------------------------------------------------------------------------------


sortedDataSet = sorted(json_list, key=lambda x: x['tag_list'][0])

print("\nWriting to file...")
t = time()


#Output topics to file
#output_to_file("ldaDataSet_Organized_Culled.json", sortedDataSet[8196:495312])
#output_to_file("ldaDataSet_Organized_Culled.json", sortedDataSet)


print("Elapsed Time: %0.3fs" % (time() - t))