from configparser import ConfigParser
from pathlib import Path


class ConfigFile:

    def __init__(self):
        self.config_file = "../config.ini"
        self.config_object = ConfigParser()
        self.config_file_dataset = "DATASET"
        self.config_file_config = "CONFIGURATION"
        self.key_config = "switch_var"
        self.switch_var_default = "off"
        self.key = ["path_training", "path_test", "test_size", "column_text", "column_target", "language",
                    "class_string", "int_classes", "name_classes"]
        self.default_values = ["../dataset/AG News/train.csv", "../dataset/AG News/test.csv", "0.3", 'Description',
                               'Class Index', "english", "False", "1, 2, 3, 4", "World, Sports, Business, Sci/Tech"]
        if not self.is_present_config_file(): self.create_default_config_file()
        self.path_training, self.path_test, self.test_size, self.column_text, self.column_target, self.language, self. \
            class_string, self.int_classes, self.name_classes = self.read_config_file()
        self.switch_var = self.read_attribute(self.config_file_config, self.key_config)

    def create_default_config_file(self):
        """
        Method to write default configuration file
        """
        self.config_object[self.config_file_dataset] = self.create_dictionary_config_file(self.default_values)
        self.config_object[self.config_file_config] = {self.key_config: self.switch_var_default}
        self.write()

    def create_dictionary_config_file(self, values):
        """
        Method compute dictionary
        :param values: array to associate value at each key
        :return: dictionary
        """
        return dict(zip(self.key, values))

    def is_present_config_file(self):
        """
        Method to compute if configuration file exists
        :return: boolean value
        """
        return True if Path(self.config_file).is_file() else False

    def read_config_file(self):
        """
        Method to read all attributes (relative to dataset) of the configuration file
        :return: array
        """
        return [self.read_attribute(self.config_file_dataset, key) for key in self.key]

    def read_attribute(self, section, attribute):
        """
        Method to read one attribute
        :param section: String of the section
        :param attribute: String of the attribute
        :return: string of read value
        """
        self.config_object.read(self.config_file)
        return self.config_object.get(section, attribute)

    def write(self):
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
        self.write()
