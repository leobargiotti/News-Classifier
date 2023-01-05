from texthero import preprocessing as ppe
import texthero as hero
import contractions
from sklearn.base import BaseEstimator, TransformerMixin
from simplemma import lemmatize
import pycountry
import nltk


class PreprocessingSteps:
    def __init__(self, X, language):
        self.X = X
        self.language = language
        self.stopwords = set(nltk.corpus.stopwords.words(self.language))

    def expanding_contractions(self):
        """
        Method to expand english contractions
        :return: itself (PreprocessingSteps)
        """
        if self.language == "english":
            self.X = self.X.apply(lambda x: contractions.fix(x))
        return self

    def clean_text(self):
        """
        Method to lowercase and remove html tags, URLs, punctuation, diacritics, digits, extra whitespaces and stopwords
        :return: itself (PreprocessingSteps)
        """
        self.X = hero.replace_urls(self.X, " ")
        self.X = hero.remove_digits(self.X, only_blocks=False)
        self.X = hero.clean(s=self.X, pipeline=[ppe.remove_html_tags, ppe.remove_punctuation, ppe.remove_diacritics, ppe.lowercase])
        for i in ["\\", "<", ">", "'", "-", '"']: self.X = self.X.apply(lambda x: x.replace(i, " "))
        self.X = hero.remove_stopwords(self.X, self.stopwords)
        self.X = hero.remove_whitespace(self.X)
        return self

    def stem(self):
        """
        Method to perform stemming
        :return: itself (PreprocessingSteps)
        """
        self.X = ppe.stem(self.X, language=self.language, stem='snowball')
        return self

    def lemma(self):
        """
        Method to perform lemmatization
        :return: itself (PreprocessingSteps)
        """
        language_code = pycountry.languages.get(name=self.language).alpha_2
        self.X = self.X.apply(lambda x: ' '.join([lemmatize(str(word), language_code) for word in nltk.word_tokenize(str(x))]))
        return self

    def get_processed_text(self):
        """
        Method to get preprocessed text
        :return: preprocessed text
        """
        return self.X


class TextPreprocessor(TransformerMixin, BaseEstimator):
    def __init__(self, language):
        self.language = language

    def fit(self, X, y=None):
        """
        Method to preprocess text
        """
        return self

    def transform(self, X, y=None):
        """
        Method to preprocess text
        """
        return PreprocessingSteps(X.copy(), self.language).expanding_contractions().clean_text().stem().lemma().get_processed_text()
