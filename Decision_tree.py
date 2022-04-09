import numpy as np
import math 
import random
def read_file(file_n):
    with open(file_n) as file:
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
    return(features)

def calculate_entropy(values):
    unique, counts = np.unique(values, return_counts=True)
    probability = [x/len(values) for x in counts]
    entropy = [-x*math.log(x, 2.0) for x in probability]
    result = 0
    for val in entropy:
        result+=val
    return result   

def get_lowest_entropy(subdict):
    entropies = {}
    labels = list(subdict[0].keys())[:len(subdict)-1]
    for label in labels:
        column = []
        for i in range(len(subdict)):
            column.append(features[i][label])
        entropy = calculate_entropy(column)
        entropies[label] = entropy
    lowest_entropy_value = min(entropies.values())
    lowest_entropy_keys = [key for key in entropies if entropies[key] == lowest_entropy_value]
    return(lowest_entropy_keys, lowest_entropy_value)

class Node:
    def __init__(self, subdict, lowest_en_feature, lowest_entropy, feature_list):
        self._subdict = subdict
        self._lowest_en_feature = lowest_en_feature
        self._entropy = lowest_entropy
        self._feature_list = feature_list
    def get_subdict(self):
        return self._subdict
    def get_feature(self):
        return self._lowest_en_feature
    def get_entropy(self):
        return self._entropy
    def get_feature_list(self):
        return self._feature_list
    
def split(node):
    new_nodes = []
    subdictionary = node.get_subdict()
    feat = node.get_feature()
    for i in range(len(subdictionary)):
        new_nodes.append(subdictionary[i][feat])
    new_nodes = (list(Counter(new_nodes).keys()))
    for val in new_nodes:
        new_subdict = {}
        for key, value in subdictionary.items():
            if subdictionary[key][feat] == val:
                new_subdict[key] = value
        feature, lowest_entr = get_lowest_entropy(new_subdict)
        labels = list((list(new_subdict.values())[0]).keys())[:len(new_subdict)-1]
        new_node = Node(new_subdict, random.choice(feature), lowest_entr, labels)
        # tree.add_node(node) is what we want to do here
        
def main():
    mydict = read_file('pets.txt')
    feature, lowest_entr = get_lowest_entropy(subdict)
    labels = list(mydict[0].keys())[:len(mydict)-1]
    node = Node(mydict, random.choice(feature), lowest_entr, labels)
    print("lowest entropy: ", node.get_entropy(), 
          "\n", "lowest entropy feature: ", node.get_feature(), 
          "\n", "feature list: ", node.get_feature_list(), 
          "\n", "node subdictionary: ", "\n", node.get_subdict())
main()
