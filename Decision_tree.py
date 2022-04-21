import numpy as np
import math 
import random
from collections import Counter
import copy
import os

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
        self._child = None
        
    def get_subdict(self):
        return self._subdict
    def get_attr(self):
        return self._attr
    def get_classifier(self):
        return self._classifier
    def get_child(self):
        return self._child
    
    def set_subdict(self,sub_dict):
        self._subdict = sub_dict
    def set_attr(self, attr):
        self._attr = attr
    def set_classifier(self, classifier):
        self._classifier = classifier
    def set_child(self, child):
        self._child = child

def get_root(features):
    goal = return_goal(features)
    classifier = []
    for i in range(len(features)):
        classifier.append(features[i][goal])
    class_val=Counter(classifier)
    proportion = sum(class_val.values())
    max_value = (max(class_val, key=class_val.get),round(max(class_val.values())/proportion,2))
    node = Node(features, None, max_value)
    return node

def build_decision_tree(curr_list, curr_node, goal): 
    stop = True
    for item in curr_list:
        if len(item)>1:
            stop = False
    if stop == True:
        return curr_node
    lb = list(curr_list[0].keys())[:-1]#size, color...
    table = convert(curr_list, gl, lb)#size{tiny:[yes, no]...} 
    entropy, feature = minimum_entropy(table)
    if entropy == 0.0:
        return 
    child = {}
    for key in table[feature]:
        temp_list = []
        class_val = Counter(table[feature][key])
        proportion = sum(class_val.values())
        max_value = (max(class_val, key=class_val.get),round(max(class_val.values())/proportion,2))
        for d in curr_list:
            if d[feature] == key:#attr = size, color...
                temp_dic = copy.deepcopy(d)
                temp_dic.pop(feature)
                temp_list.append(temp_dic)

        node = Node (temp_list, key, max_value)
        child[key]=node
        curr_node.set_child(child)
        build_decision_tree(temp_list,node,goal)
        

def user_dic(line_input,inital_dic):#does not handle cases where the user inputs attribute in different order
    labels = list(inital_dic[0].keys())
    del labels[-1]
    attributes = line_input.split()
    query_dic = {}
    for i in range(len(labels)):
        query_dic[labels[i]]=attributes[i]
    return query_dic
        
def query(query_dic, curr_node):
    if len(query_dic)==0 or curr_node.get_child()==None:
        return (curr_node.get_classifier())
    
    for key,value in list(query_dic.items()):
        if value in list(curr_node.get_child().keys()):
            temp_query = copy.deepcopy(query_dic)
            del temp_query[key]
            return query(temp_query,curr_node.get_child()[value])
        else:
            return curr_node.get_classifier()

def cross_validation(input_file):
    with open(input_file) as file:
        data = file.readlines()
    lines_list = []
    labels_line = data[0]
    for line in data[1:]:
        lines_list.append(line)
    for i in range(len(lines_list)):
        if os.path.exists("testing.txt"):
            os.remove("testing.txt")
        test_input = copy.deepcopy(lines_list)
        test_input.pop(i)
        f = open("testing.txt", "a")
        f.write(labels_line)
        for item in test_input:
            f.write(item)
        f.close()
        tb, lb =read_file("testing.txt")
        gl = return_goal(tb)
        root = get_root(tb)
        accurate_tb, accurate_lb = read_file(input_file)
        accurate_root = get_root(accurate_tb)
        build_decision_tree(accurate_tb, accurate_root, gl)
        build_decision_tree(tb, root, gl)
        input_dict = user_dic(lines_list[i], tb)
        print("testing input: ", input_dict)
        print("classification: ", query(input_dict, root), query(input_dict, accurate_root), 
              query(input_dict, root)[0] == query(input_dict, accurate_root)[0] )
        print()

        
        
tb, lb = read_file('pets.txt')
gl = return_goal(tb)
#root = get_root(tb)
#line = "small	orange	pointed	yes"
#build_decision_tree(tb, root, gl)
#dic = user_dic(line,tb)
cross_validation('pets.txt')
