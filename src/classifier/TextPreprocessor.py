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

    def expanding_contractions(self, flag_expanding_contractions):
        """
        Method to expand english contractions
        :param flag_expanding_contractions: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = self.X.apply(lambda x: contractions.fix(x)) if self.language == "english" and flag_expanding_contractions else self.X
        return self

    def remove_html_tags(self, flag_html_tags):
        """
        Method to remove html tags
        :param flag_html_tags: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = ppe.remove_html_tags(self.X) if flag_html_tags else self.X
        return self

    def remove_urls(self, flag_urls):
        """
        Method to remove urls
        :param flag_urls: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = hero.replace_urls(self.X, " ") if flag_urls else self.X
        return self

    def remove_punctuation(self, flag_punctuation):
        """
        Method to remove punctuation
        :param flag_punctuation: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        if flag_punctuation:
            self.X = ppe.remove_punctuation(self.X)
            for i in ["\\", "<", ">", "'", "-", '"']: self.X = self.X.apply(lambda x: x.replace(i, " "))
        return self

    def remove_diacritics(self, flag_diacritics):
        """
        Method to remove diacritics
        :param flag_diacritics: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = ppe.remove_diacritics(self.X) if flag_diacritics else self.X
        return self

    def lowercase(self, flag_lowercase):
        """
        Method to lowercase
        :param flag_lowercase: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = ppe.lowercase(self.X) if flag_lowercase else self.X
        return self

    def remove_digits(self, flag_digits):
        """
        Method to remove digits
        :param flag_digits: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = hero.remove_digits(self.X, only_blocks=False) if flag_digits else self.X
        return self

    def remove_extra_whitespace(self, flag_extra_whitespace):
        """
        Method to remove extra whitespace
        :param flag_extra_whitespace: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = hero.remove_whitespace(self.X) if flag_extra_whitespace else self.X
        return self

    def remove_stopwords(self, flag_stopwords):
        """
        Method to remove stopwords
        :param flag_stopwords: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = hero.remove_stopwords(self.X, self.stopwords) if flag_stopwords else self.X
        return self

    def stem(self, flag_stem):
        """
        Method to perform stemming
        :paramn flag_stem: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = ppe.stem(self.X, language=self.language, stem='snowball') if flag_stem else self.X
        return self

    def lemma(self, flag_lemma):
        """
        Method to perform lemmatization
        :param flag_lemma: boolean value if true apply function otherwise not
        :return: itself (PreprocessingSteps)
        """
        self.X = self.X.apply(lambda x: ' '.join([lemmatize(str(word), pycountry.languages.get(name=self.language).alpha_2)
                                                  for word in nltk.word_tokenize(str(x))])) if flag_lemma else self.X
        return self

    def get_processed_text(self):
        """
        Method to get preprocessed text
        :return: preprocessed text
        """
        return self.X


class TextPreprocessor(TransformerMixin, BaseEstimator):
    def __init__(self, language, stopwords, stemming, lemma, digits, expanding_contractions, urls, html_tags, punctuation,
                 diacritics, lowercase, extra_whitespace):
        self.language = language
        self.stopwords = stopwords
        self.stemming = stemming
        self.lemma = lemma
        self.digits = digits
        self.expanding_contractions = expanding_contractions
        self.urls = urls
        self.html_tags = html_tags
        self.punctuation = punctuation
        self.diacritics = diacritics
        self.lowercase = lowercase
        self.extra_whitespace = extra_whitespace

    def fit(self, X, y=None):
        """
        Method to preprocess text
        """
        return self

    def transform(self, X, y=None):
        """
        Method to preprocess text
        """
        return PreprocessingSteps(X.copy(), self.language)\
            .expanding_contractions(self.expanding_contractions)\
            .remove_urls(self.urls)\
            .remove_digits(self.digits)\
            .remove_html_tags(self.html_tags)\
            .remove_punctuation(self.punctuation)\
            .remove_diacritics(self.diacritics)\
            .lowercase(self.lowercase)\
            .remove_stopwords(self.stopwords)\
            .remove_extra_whitespace(self.extra_whitespace)\
            .stem(self.stemming)\
            .lemma(self.lemma)\
            .get_processed_text()
