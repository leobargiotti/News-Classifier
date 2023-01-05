import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import json
import nltk


def calculate_training_test(train, test, config_file):
    """
    Method to compute training and test set
    :param train: training dataframe
    :param test: test dataframe
    :param config_file: configuration file
    :return: list containing train-test split
    """
    test_size, column_text, column_target = config_file.test_size, config_file.column_text, config_file.column_target
    X = train[column_text]
    y = train[column_target]
    if test is None:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(test_size), random_state=0)
    else:
        X_train = X
        y_train = y
        X_test = test[column_text]
        y_test = test[column_target]
    return X_train, X_test, y_train, y_test


def calculate_train_test_classes(train, test, config_file):
    """
    Method to compute training, test set and dictionary of the classes
    :param train: training dataframe
    :param test: test dataframe
    :param config_file: configuration file
    :return: list containing train-test split and dictionary of the classes
    """
    class_string, int_classes, name_classes = config_file.class_string, config_file.int_classes, config_file.\
        name_classes
    X_train, X_test, y_train, y_test = calculate_training_test(train, test, config_file)
    if not json.loads(class_string.lower()):
        classes = create_dictionary_classes(int_classes, name_classes)
    else:
        y_train, y_test, classes = encode_label_classes(y_train, y_test)
    return X_train, X_test, y_train, y_test, classes


def encode_label_classes(y_train, y_test):
    """
    Method to compute training, test to encode and dictionary of the classes
    :param y_train: y_training dataframe
    :param y_test: y_test dataframe
    :return: list containing train-test encoded and dictionary of the classes
    """
    le = LabelEncoder()
    y_train_new = pd.Series(le.fit_transform(y_train))
    y_test_new = pd.Series(le.fit_transform(y_test))
    classes = dict(zip(range(len(le.classes_)), le.classes_))
    return y_train_new, y_test_new, classes


def create_dictionary_classes(int_classes, name_classes):
    """
    Method to compute dictionary of the classes
    :param int_classes: list of integer value of classes
    :param name_classes: list of strings value of classes
    :return: dictionary that associates integer to string value of classes
    """
    name_class = name_classes.split(",")
    name_class = [name_class[x].strip() for x in range(len(name_class))]
    int_class = int_classes.split(",")
    int_class = [int(int_class[x]) for x in range(len(int_class))]
    return dict(zip(int_class, name_class))


def drop_duplicates_and_nan(data, column_text, column_target):
    """
    Method to remove duplicates and Nan values
    :param data: dataframe to remove duplicates and Nan values
    :param column_text: string of column name that contains text
    :param column_target: string of column name that contains classes
    :return: dataframe without duplicates and Nan values
    """
    data = data.drop_duplicates(subset=[column_text, column_target])
    data = data.dropna()
    return data


def remove_duplicates_and_nan_values(config_file):
    """
    Method to remove duplicates and Nan values
    :param config_file: configuration file
    :return: list containing train-test dataframe without duplicates and Nan values
    """
    path_train, path_test, column_text, column_target = config_file.path_training, config_file.path_test, \
                                                         config_file.column_text, config_file.column_target
    train_original = pd.read_csv(path_train)
    train_cleaned = drop_duplicates_and_nan(train_original, column_text, column_target)
    if not str(path_test).lower() == "null":
        test_original = pd.read_csv(path_test)
        test_cleaned = drop_duplicate_and_nan(test_original, column_text, column_target)
        return train_original, train_cleaned, test_original, test_cleaned
    else:
        return train_original, train_cleaned, None, None


def download_if_non_existent(res_path, res_name):
    """
    Method to download nltk package only if it is not downloaded
    :param res_path: string local directory of the package
    :param res_name: string name of package
    """
    try:
        nltk.data.find(res_path)
    except LookupError:
        print(f'resource {res_path} not found. Downloading now...')
        nltk.download(res_name)
