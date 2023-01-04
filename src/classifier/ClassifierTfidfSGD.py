from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold

from .Classifier import Classifier


class ClassifierTfidfSGD(Classifier):

    def __init__(self):
        Classifier.__init__(self, "../model_saved/TfidfSGD.pk")

    def create_pipeline(self):
        """
        Method to instance Pipeline with classifier
        :return: Pipeline with TextPreprocessor, TfidfVectorizer and SGDClassifier
        """
        return Pipeline(super().create_pipeline().steps.__add__([
            ('sgd', GridSearchCV(SGDClassifier(random_state=0),
                                 param_grid={'eta0': [0.0, 0.03, 0.01, 0.003, 0.001, 0.0003],
                                             'penalty': ['l1', 'l2', 'elasticnet'],
                                             'alpha': [1, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001, 0.0003, 0.0001],
                                             'loss': ['log_loss', 'modified_huber']},
                                 cv=StratifiedKFold(),
                                 scoring='accuracy'))]))
