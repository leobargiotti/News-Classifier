import numpy as np
import dill as pickle
import pandas as pd
from pathlib import Path
import os
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from utils.utils import calculate_train_test_classes, remove_duplicates_and_nan_values
from .TextPreprocessor import TextPreprocessor
from configuration.ConfigFile import ConfigFile


class Classifier:
    def __init__(self, path_pipeline):
        self.name = str(self.__class__).split(".")[- 2]
        self.path_pipeline = path_pipeline
        self.config_file = ConfigFile()
        self.train_original, self.train_cleaned, self.test_original, self.test_cleaned = remove_duplicates_and_nan_values(self.config_file)
        self.X_train, self.X_test, self.y_train, self.y_test, self.classes = calculate_train_test_classes(
            self.train_cleaned, self.test_cleaned, self.config_file)
        if not self.is_present_model(): self.create_model()
        self.model = self.load_model()

    def reload_config(self):
        """
        Method to recreate the classifier
        """
        if Path(self.path_pipeline).is_file(): os.remove(self.path_pipeline)
        self.__init__()

    def save_model(self):
        """
        Method save the classifier in local folder
        """
        pickle.dump(self.model, open(self.path_pipeline, 'wb'))

    def load_model(self):
        """
        Method to load the classifier
        :return: classifier
        """
        return pickle.load(open(self.path_pipeline, 'rb'))

    def is_present_model(self):
        """
        Method to compute if classifier is saved in the local folder
        :return: boolean value
        """
        return True if Path(self.path_pipeline).is_file() else False

    def create_model(self):
        """
        Method to fit the classifier with GridSearchCV
        """
        t0 = time.time()
        print("The classifier " + self.name + " is fitting...")
        self.model = self.create_pipeline().fit(self.X_train, self.y_train.values.ravel())
        print("The classifier " + self.name + " is created with this parameters: " +
              str(self.model[2].best_params_) + ", with a best score of " + str(round(self.model[2].best_score_, 3)) +
              " in " + str(round(time.time() - t0, 3)) + " seconds")
        self.save_model()

    def print_class(self, int_class):
        """
        Method to compute the name of the class
        :param int_class: integer of the class
        :return: string of the class
        """
        return self.classes.get(int_class)

    def create_pipeline(self):
        """
        Method to instance Pipeline without classifier (GridSearchCV)
        :return: Pipeline with TextPreprocessor and TfidfVectorizer
        """
        return Pipeline([
            ('text_preproc', TextPreprocessor(language=self.config_file.language)),
            ('tfidf', TfidfVectorizer(encoding='utf-8', ngram_range=(1, 2), stop_words=None,
                                      lowercase=False, max_df=0.95, min_df=10, norm='l2', sublinear_tf=True))])

    def calculate_class(self, text):
        """
        Method to compute predict of a classifier
        :param text: Dataframe to calculate prediction
        :return: string of predicted class and its probability
        """
        y_prob = self.model.predict_proba(pd.Series(text))
        return "Class predicted is: " + self.print_class(self.model.predict(pd.Series(text))[0]) \
               + "\nand its probability is: " + str(round(y_prob[0][np.argmax(y_prob)] * 100, 2)) + "%"
