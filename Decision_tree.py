import numpy as np
import math 
import random
from collections import Counter
def read_file(file_n):
    with open(file_n) as file:
        data = file.readlines()
        labels = data[0].split()
        lines = []
        features={}
        for i in range(len(data[1:])):
            line = data[i+1].split()
            tempdict = {}
            for j in range(len(labels)):
                tempdict[labels[j]] = line[j]
                features[i] = tempdict
    return(features)

def return_goal(table): 
    return list(list(table.values())[0].keys())[-1]

def minimum_entropy(table, goal): #table is a dictionary of each line in the dataset
    labels = list(list(table.values())[0].keys())[:-1]
    evaluate = []
    attribute_split = {}
    for label in labels:
        column = []
        for i in range(len(table)):
            column.append(table[i][label])
        feature_dict = Counter(column) 
        new_dict = {}
        for key in feature_dict.keys():
            temp = []
            for i in range(len(table)):
                if table[i][label] == key:
                    temp.append(table[i][goal])
            new_dict[key] = temp
        attribute_split[label] = new_dict
        epy = []
        for i in range(len(new_dict)):
            unique, counts = np.unique(list(new_dict.values())[i], return_counts=True)
            proportion = sum(counts)
            probability = [p/len(list(new_dict.values())[i]) for p in counts]
            entropy = [-x*math.log(x, 2.0) for x in probability]
            result = 0
            for val in entropy:
                result+=val
            epy.append(result*proportion/len(table))
        feature_entropy = (sum(epy),label)
        evaluate.append(feature_entropy)
    attr = attribute_split[min(evaluate)[1]]
    return attr, min(evaluate)[1]

def calculate_entropy(inp_attr): #this is a dictionary of attr as keys  and goal mappings as values
    entropy_values = {}
    for key in inp_attr.keys():
        values = inp_attr[key]
        unique, counts = np.unique(values, return_counts=True)
        probability = [p/len(values) for p in counts]
        entropy = [-x*math.log(x, 2.0) for x in probability]
        result = 0
        for val in entropy:
            result+=val
        entropy_values[key] = result
    return entropy_values

class Node:
    def __init__(self, subdict, attr, entropy, classifier):
        self._subdict = subdict
        self._attr = attr
        self._classifier = classifier
        self._entropy = entropy
        
    def get_subdict(self):
        return self._subdict
    def get_attr(self):
        return self._attr
    def get_classifier(self):
        return self._classifier
    def get_entropy(self):
        return self._entropy
    
    def set_subdict(self,sub_dict):
        self._subdict = sub_dict
    def set_attr(self, attr):
        self._attr = attr
    def set_classifier(self, classifier):
        self._classifier = classifier
    def set_entropy(self, entropy):
        self._entropy = entropy

def get_root(features):
    goal = return_goal(features)
    column = []
    for i in range(len(features)):
        column.append(features[i][goal])
    entr = Counter(column)
    max_value = max(entr, key = entr.get)
    node = Node(features, None, None, max_value )
    return node

def build_decision_tree(curr_dictionary,parent):
    if len(curr_dictionary[0]) == 1:
        return parent.get_classifier()
    goal = return_goal(curr_dictionary)
    feat_dict, split = minimum_entropy(curr_dictionary, goal)
    attribute_entr = calculate_entropy(feat_dict)
    for i in range(len(curr_dictionary)):
        curr_dictionary[i].pop(split)
    count=0
    for key in attribute_entr.keys():
        temp_dict = Counter(feat_dict[key])
        entropy= attribute_entr[key]
        max_value = max(temp_dict, key=temp_dict.get)
        node = Node(curr_dictionary, key, entropy, max_value)
        print(node.get_subdict(), node.get_attr(), node.get_classifier(), node.get_entropy())
        print()
        print()
        if node.get_entropy()==0.0:
            return node.get_classifier()
        else:
            build_decision_tree(curr_dictionary,node) 

def main(input_file):
    features = read_file(input_file)
    root = get_root(features)
    #print(root.get_classifier())
    build_decision_tree(features, root)
main('pets.txt') 
