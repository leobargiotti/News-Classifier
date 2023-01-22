from texthero import preprocessing as ppe
import texthero as hero
import contractions
from sklearn.base import BaseEstimator, TransformerMixin
from simplemma import lemmatize
import pycountry
import nltk


class PreprocessingSteps:
    def __init__(self, X, language, config_file):
        self.X = X
        self.language = language
        self.stopwords = set(nltk.corpus.stopwords.words(self.language))
        self.config_file = config_file

    def expanding_contractions(self):
        """
        Method to expand english contractions
        :return: itself (PreprocessingSteps)
        """
        self.X = self.X.apply(lambda x: contractions.fix(x)) if self.language == "english" and self.config_file.expanding_contractions else self.X
        return self

    def remove_html_tags(self):
        """
        Method to remove html tags
        :return: itself (PreprocessingSteps)
        """
        self.X = ppe.remove_html_tags(self.X) if self.config_file.html_tags else self.X
        return self

    def remove_urls(self):
        """
        Method to remove urls
        :return: itself (PreprocessingSteps)
        """
        self.X = hero.replace_urls(self.X, " ") if self.config_file.urls else self.X
        return self

    def remove_punctuation(self):
        """
        Method to remove punctuation
        :return: itself (PreprocessingSteps)
        """
        if self.config_file.punctuation:
            self.X = ppe.remove_punctuation(self.X)
            for i in ["\\", "<", ">", "'", "-", '"']: self.X = self.X.apply(lambda x: x.replace(i, " "))
        return self

    def remove_diacritics(self):
        """
        Method to remove diacritics
        :return: itself (PreprocessingSteps)
        """
        self.X = ppe.remove_diacritics(self.X) if self.config_file.diacritics else self.X
        return self

    def lowercase(self):
        """
        Method to lowercase
        :return: itself (PreprocessingSteps)
        """
        self.X = ppe.lowercase(self.X) if self.config_file.lowercase else self.X
        return self

    def remove_digits(self):
        """
        Method to remove digits
        :return: itself (PreprocessingSteps)
        """
        self.X = hero.remove_digits(self.X, only_blocks=False) if self.config_file.digits else self.X
        return self

    def remove_extra_whitespace(self):
        """
        Method to remove extra whitespace
        :return: itself (PreprocessingSteps)
        """
        self.X = hero.remove_whitespace(self.X) if self.config_file.extra_whitespace else self.X
        return self

    def remove_stopwords(self):
        """
        Method to remove stopwords
        :return: itself (PreprocessingSteps)
        """
        self.X = hero.remove_stopwords(self.X, self.stopwords) if self.config_file.stopwords else self.X
        return self

    def stem(self):
        """
        Method to perform stemming
        :return: itself (PreprocessingSteps)
        """
        self.X = ppe.stem(self.X, language=self.language, stem='snowball') if self.config_file.stemming else self.X
        return self

    def lemma(self):
        """
        Method to perform lemmatization
        :return: itself (PreprocessingSteps)
        """
        self.X = self.X.apply(lambda x: ' '.join([lemmatize(str(word), pycountry.languages.get(name=self.language).alpha_2)
                                                  for word in nltk.word_tokenize(str(x))])) if self.config_file.lemma else self.X
        return self

    def get_processed_text(self):
        """
        Method to get preprocessed text
        :return: preprocessed text
        """
        return self.X


class TextPreprocessor(TransformerMixin, BaseEstimator):
    def __init__(self, language, config_file):
        self.language = language
        self.config_file = config_file

    def fit(self, X, y=None):
        """
        Method to preprocess text
        """
        return self

    def transform(self, X, y=None):
        """
        Method to preprocess text
        """
        return PreprocessingSteps(X.copy(), self.language, self.config_file).expanding_contractions().remove_urls()\
            .remove_digits().remove_html_tags().remove_punctuation().remove_diacritics().lowercase().remove_stopwords()\
            .remove_extra_whitespace().stem().lemma().lowercase().get_processed_text()
