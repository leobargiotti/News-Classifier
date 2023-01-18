from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from warnings import simplefilter

from .Classifier import Classifier


class ClassifierTfidfLogReg(Classifier):
    def __init__(self):
        Classifier.__init__(self, "../models_saved/TfidfLogReg.pk")

    def build_pipeline(self):
        """
        Method to instance Pipeline with classifier
        :return: Pipeline with TextPreprocessor, TfidfVectorizer and LogisticRegression
        """

        print(self.config_file.hide_warning_log_reg)

        if self.config_file.hide_warning_log_reg:
            simplefilter(action='ignore', category=UserWarning)
            simplefilter(action="ignore", category=RuntimeWarning)

        return Pipeline(super().build_pipeline().steps.__add__([
            ('lgr', GridSearchCV(LogisticRegression(penalty='l2'),
                                 param_grid={'C': [100, 75, 50, 25, 15, 10, 5, 3, 1, 0.1, 0.05, 0.01],
                                 'solver': ['liblinear', 'newton-cg']},
                                 cv=StratifiedKFold(), scoring='accuracy',
                                 verbose=3 if self.config_file.debug_classifier else 0))]))
