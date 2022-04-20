import numpy as np
import math 
import random
from collections import Counter
import copy

def read_file(file_n):
    with open(file_n) as file:
        data = file.readlines()
        labels = data[0].split()
        lines = []
        features=[]
        for i in range(len(data[1:])):
            line = data[i+1].split()
            tempdict = {}
            for j in range(len(labels)):
                tempdict[labels[j]] = line[j]
            features.append(tempdict)
    return features, labels[:-1]

def return_goal(table): 
    return list(table[0].keys())[-1]

def convert(table, goal, labels): #table is a list of each line in the dataset
    evaluate = []
    attribute_split = {}
    for label in labels:
        column = []
        for i in range(len(table)):
            column.append(table[i][label])
        feature_dict = Counter(column) 
        new_dict = {}
        #print(label, feature_dict)
        for key in feature_dict.keys():
            temp = []
            for i in range(len(table)):
                if table[i][label] == key:
                    temp.append(table[i][goal])
            new_dict[key] = temp
        attribute_split[label] = new_dict
    return attribute_split

def minimum_entropy(table):
    
    labels = list(table.keys())
    list_feat_entropies = []
    for label in range(len(labels)):
        lenght= list(list(table.values())[label].values())[:]
        possible_vals = 0
        for i in lenght:
            possible_vals+=(len(i))
        feature_entropy =[]
        for i in lenght:
            unique, counts = np.unique(i, return_counts=True)
            proportion = sum(counts)
            probability = [p/proportion for p in counts]
            attr_entropy = [-x*math.log(x, 2.0) for x in probability]
            result = 0
            for val in attr_entropy:
                result+=val
            feature_entropy.append(result*proportion/possible_vals)
        list_feat_entropies.append((sum(feature_entropy),labels[label]))
    return min(list_feat_entropies)

class Node:
    def __init__(self, subdict, attr, classifier):
        self._subdict = subdict
        self._attr = attr
        self._classifier = classifier
        
    def get_subdict(self):
        return self._subdict
    def get_attr(self):
        return self._attr
    def get_classifier(self):
        return self._classifier
    
    def set_subdict(self,sub_dict):
        self._subdict = sub_dict
    def set_attr(self, attr):
        self._attr = attr
    def set_classifier(self, classifier):
        self._classifier = classifier

def get_root(features):
    goal = return_goal(features)
    node = Node(features, None, None )
    return node

def build_decision_tree(curr_list, parent, goal): 
    stop = True
    for item in curr_list:
        if len(item)>1:
            stop = False
    print()
    if stop == True:
        return parent
    lb = list(curr_list[0].keys())[:-1]#size, color...
    table = convert(curr_list, gl, lb)#size{tiny:[yes, no]...} 
    entropy, attribute = minimum_entropy(table)
    if entropy == 0.0:
        return
    for key in table[attribute]:
        temp_list = []
        for d in curr_list:
            if d[attribute] == key:#attr = size, color...
                temp_dic = copy.deepcopy(d)
                temp_dic.pop(attribute)
                temp_list.append(temp_dic)
                
        node = Node (temp_list, key, goal)
        print(node.get_subdict(),node.get_attr())
        
        build_decision_tree(temp_list,node,goal)

tb, lb = read_file('pets.txt')
gl = return_goal(tb)
root = get_root(tb)
build_decision_tree(tb, root, gl)
