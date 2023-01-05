from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from .Classifier import Classifier


class ClassifierTfidfLogReg(Classifier):

    def __init__(self):
        Classifier.__init__(self, "../models_saved/TfidfLogReg.pk")

    def create_pipeline(self):
        """
        Method to instance Pipeline with classifier
        :return: Pipeline with TextPreprocessor, TfidfVectorizer and LogisticRegression
        """
        return Pipeline(super().create_pipeline().steps.__add__([
            ('lgr', GridSearchCV(LogisticRegression(penalty='l2'),
                                 param_grid={'C': [25, 20, 15, 10, 5, 3, 1, 0.1, 0.05, 0.01],
                                 'solver': ['liblinear', 'newton-cg']},
                                 cv=StratifiedKFold(),
                                 scoring='accuracy'))]))
