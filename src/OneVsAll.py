#!/usr/bin/env python 
'''
A container class for running OneVsAll operations for a generic binary classifier that implements
train()
predict(feature_vector) -> confidence_measure (/regressed value)
test(feature_vector, true_label) -> boolean

see BLRegression.py for an example
'''
import numpy as np
from Point import Point
from LogReader import LogReader
from BLRegression import BLRegression

class OneVsAll:
    def __init__(self, features, labels, classifier_class, classifier_params, test_features = None, test_labels = None):
               
        if test_features is None:
            self.X = np.array(features)
            self.Y = np.array(labels)
            
            hold_out_index = self.X.shape[0]*0.8
            
            self.trainX = self.X[:hold_out_index,:]
            self.trainY = self.Y[:hold_out_index]
            
            self.testX  = self.X[hold_out_index:, :]
            self.testY  = self.Y[hold_out_index:]
        else:
            self.trainX = np.array(features)
            self.trainY = np.array(labels)
            
            self.testX = np.array(test_features)
            self.testY = np.array(test_labels)
        
        self.classifier_class = classifier_class
        self.classifier_params = classifier_params
        self.classifiers = []
        
        
    def train(self):
        print '[OneVsAll] Training individual predictors...'
        for label in Point.label_dict:
            #Separate the data into positive and negative classes
            trainY = self.trainY.copy()
            trainY[trainY != Point.label_dict[label]] = -1
            trainY[trainY != -1] = 1
            
            #Train the classifier
            classifier = self.classifier_class(self.trainX, trainY, self.classifier_params)
            classifier.train()
            self.classifiers.append(classifier)
            print '[OneVsAll] Trained ', label
        print '[OneVsAll] Done!'
        
    def predict(self, dataX):
        #Check if sane data point
        assert(dataX.shape == self.trainX[0].shape)
        predicted_confidences = [classifier.predict(dataX) for classifier in self.classifiers]
        classifier_index = predicted_confidences.index(max(predicted_confidences))
        return classifier_index
    
    def test(self):
        evals = []
        for index in range(len(self.testX)):
            dataX = self.testX[index]
            true_label = self.testY[index]
            classifier_index = self.predict(dataX)
            evals.append(self.classifiers[classifier_index].test(dataX, true_label))
        #Now evaluate accuracy
        #True == 1, thus sum
        print '[OneVsAll] Accuracy = ', float(sum(evals))/len(evals)
        
        
if __name__ == "__main__":
    #Sample implementation for a Bayes Linear Classifier
    #Load a log
    train_log_object = LogReader('../data/oakland_part3_am_rf.node_features')
    train_points = train_log_object.read()
    test_log_object = LogReader('../data/oakland_part3_an_rf.node_features')
    test_points = test_log_object.read()
    
    bl_params = [0.2, 0.0, 1.0]
    
#     orchestrator = OneVsAll([point._feature for point in train_points], [point._label for point in train_points], BLRegression)
    orchestrator = OneVsAll([point.add_corrupted_features(1) for point in train_points], [point._label for point in train_points], 
                            BLRegression, bl_params,
                            [point.add_corrupted_features(1) for point in test_points], [point._label for point in test_points])
    orchestrator.train()
    orchestrator.test()