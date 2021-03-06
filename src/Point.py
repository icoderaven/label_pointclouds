#!/usr/bin/env python 
'''
A simple class for defining Points
'''
import numpy as np
import pdb

class Point:
    
    label_dict = {'1004':0, '1100':1, '1103':2, '1200':3, '1400':4} 
    label_rev_dict = {v: k for k, v in label_dict.items()}
    label_human = {0:'Veg', 1:'Wire', 2:'Pole', 3:'Ground', 4:'Facade'}
        
    def __init__(self, x=0.0, y=0.0, z=0.0, label=0, feature=[]):
        self._x = x 
        self._y = y
        self._z = z
        self._label = label
        self._feature = np.array(feature)
    
    def add_random_features(self, num_features):
        return np.append(self._feature, np.random.rand(num_features)) 
    
    def add_corrupted_features(self, num_copies=1):
        a =np.array([])
        for i in range(num_copies):
            a = np.append(a, np.random.normal(self._feature, 0.1) )
        return a 