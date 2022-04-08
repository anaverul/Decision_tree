import numpy as np
import math as mh

def read_file(file_n):
    with open(file_n) as file: # Use file to refer to the file object
        data = file.readlines()
        labels = data[0].split()
        lines = []
        features={}

        for i in range(len(data[1:])):
            line = data[i+1].split()
            tempdict = {}
            for j in range(len(labels)-1):
                tempdict[labels[j]] = line[j]
                features[i] = tempdict
    for i in range(len(features)):
        print(features[i]['size'])
    return(features)
read_file("pets.txt")

def get_entropy(feature_dict, feature):
    feature_column = ([feature_dict[i][feature] for i in list(range(len(features)))])
    values, counts = np.unique(feature, return_counts=True)#counts is in descending order
    probability = [x/len(feature_column) for x in counts]
    entropy = [-x*math.log(x, 2.0) for x in probability]
    result = 0
    for val in entropy:
        result+=val
    return result
