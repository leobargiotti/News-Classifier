from configparser import ConfigParser
from pathlib import Path
import json

from utils.utils import create_dictionary, safe_execute


class ConfigFile:
    config_file = "../config.ini"
    config_dataset = "DATASET"
    keys_dataset = ["path_training", "path_test", "test_size", "column_text", "column_target", "language",
                    "class_string", "int_classes", "name_classes"]
    dataset_default = ["../dataset/AG News/train.csv", "../dataset/AG News/test.csv", "0.3", 'Description',
                       'Class Index', "english", "False", "1, 2, 3, 4", "World, Sports, Business, Sci/Tech"]
    config_configuration = "CONFIGURATION"
    key_switch_var = "switch_var"
    switch_var_default = "off"
    config_debug = "DEBUG"
    keys_debug = ["debug_classifier", "hide_warning_log_reg"]
    debug_default = ["False", "True"]
    config_preprocess = "PREPROCESS"
    keys_preprocess = ["stopwords", "stemming", "lemmatization", "digits", "expanding_contractions", "urls", "html_tags",
                       "punctuation", "diacritics", "lowercase", "extra_whitespace", "use_idf", "n_grams", "max_df", "min_df"]
    preprocess_default = ["True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True", "True",
                          "1, 2", "0.95", "10"]

    def __init__(self):
        self.config_object = ConfigParser()
        if not self.is_present_config_file(): self.create_default_config_file()
        self.path_training, self.path_test, self.test_size, self.column_text, self.column_target, self.language, \
            self.class_string, self.int_classes, self.name_classes = self.read_all_attributes_section(self.config_dataset, self.keys_dataset)
        self.switch_var = self.read_attribute(self.config_configuration, self.key_switch_var)
        self.debug_classifier, self.hide_warning_log_reg = self.read_all_attributes_section(self.config_debug, self.keys_debug)
        self.stopwords, self.stemming, self.lemma, self.digits, self.expanding_contractions, self.urls, self.html_tags, self.punctuation,\
            self.diacritics, self.lowercase, self.extra_whitespace, self.use_idf, self.n_grams, self.max_df, self.min_df = \
            self.read_all_attributes_section(self.config_preprocess, self.keys_preprocess)

    def create_default_config_file(self):
        """
        Method to write default configuration file
        """
        self.config_object[self.config_dataset] = create_dictionary(self.keys_dataset, self.dataset_default)
        self.config_object[self.config_configuration] = {self.key_switch_var: self.switch_var_default}
        self.config_object[self.config_debug] = create_dictionary(self.keys_debug, self.debug_default)
        self.config_object[self.config_preprocess] = create_dictionary(self.keys_preprocess, self.preprocess_default)
        self.write_config_file()

    def is_present_config_file(self):
        """
        Method to compute if configuration file exists
        :return: boolean value
        """
        return True if Path(self.config_file).is_file() else False

    def read_all_attributes_section(self, section, attributes):
        """
        Method to read all attributes of the section
        :param section: String of the section
        :param attributes: Array of the attributes of the section
        :return: array
        """
        return [safe_execute(self.read_attribute(section, attribute), json.decoder.JSONDecodeError, json.loads,
                                  self.read_attribute(section, attribute).lower()) for attribute in attributes]

    def read_attribute(self, section, attribute):
        """
        Method to read one attribute
        :param section: String of the section
        :param attribute: String of the attribute
        :return: string of read value
        """
        self.config_object.read(self.config_file)
        return self.config_object.get(section, attribute)

    def write_config_file(self):
        """
        Method to write configuration file
        """
        self.config_object.write(open(self.config_file, 'w'))

    def update_config_file(self, section, attribute, new_value):
        """
        Method to write configuration file
        :param section: string of the section
        :param attribute: string of the attribute
        :param new_value: string of the new value
        """
        self.config_object.read(self.config_file)
        self.config_object.set(section, attribute, new_value)
        self.write_config_file()
