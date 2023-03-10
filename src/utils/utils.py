import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import nltk


def calculate_training_test(train, test, config_file):
    """
    Method to compute training and test set
    :param train: training dataframe
    :param test: test dataframe
    :param config_file: configuration file
    :return: list containing train-test split
    """
    X, y = train[config_file.column_text], train[config_file.column_target]
    if test is None: X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config_file.test_size, random_state=0)
    else: X_train, y_train, X_test, y_test = X, y, test[config_file.column_text], test[config_file.column_target]
    return X_train, X_test, y_train, y_test


def calculate_train_test_classes(train, test, config_file):
    """
    Method to compute training, test set and dictionary of the classes
    :param train: training dataframe
    :param test: test dataframe
    :param config_file: configuration file
    :return: list containing train-test split and dictionary of the classes
    """
    X_train, X_test, y_train, y_test = calculate_training_test(train, test, config_file)
    if not config_file.class_string: classes = create_dictionary_classes(config_file.int_classes, config_file.name_classes)
    else: y_train, y_test, classes = encode_label_classes(y_train, y_test)
    return X_train, X_test, y_train, y_test, classes


def encode_label_classes(y_train, y_test):
    """
    Method to compute training, test to encode and dictionary of the classes
    :param y_train: y_training dataframe
    :param y_test: y_test dataframe
    :return: list containing train-test encoded and dictionary of the classes
    """
    le = LabelEncoder()
    return pd.Series(le.fit_transform(y_train)), pd.Series(le.fit_transform(y_test)), \
        create_dictionary(range(len(le.classes_)), le.classes_)


def create_dictionary_classes(int_classes, name_classes):
    """
    Method to compute dictionary of the classes
    :param int_classes: list of integer value of classes
    :param name_classes: list of strings value of classes
    :return: dictionary that associates integer to string value of classes
    """
    return create_dictionary([int(x) for x in int_classes.split(",")], [x.strip() for x in name_classes.split(",")])


def create_dictionary(keys, values):
    """
    Method compute dictionary
    :param keys: array to of keys
    :param values: array to associate value at each key
    :return: dictionary
    """
    return dict(zip(keys, values))


def drop_duplicates_and_nan(data, column_text, column_target):
    """
    Method to remove duplicates and Nan values
    :param data: dataframe to remove duplicates and Nan values
    :param column_text: string of column name that contains text
    :param column_target: string of column name that contains classes
    :return: dataframe without duplicates and Nan values
    """
    return data.drop_duplicates(subset=[column_text, column_target]).dropna()


def remove_duplicates_and_nan_values(config_file):
    """
    Method to remove duplicates and Nan values
    :param config_file: configuration file
    :return: list containing train-test dataframe without duplicates and Nan values
    """
    train_original = pd.read_csv(config_file.path_training)
    train_cleaned = drop_duplicates_and_nan(train_original, config_file.column_text, config_file.column_target)
    if config_file.path_test is not None:
        test_original = pd.read_csv(config_file.path_test)
        test_cleaned = drop_duplicates_and_nan(test_original, config_file.column_text, config_file.column_target)
        return train_original, train_cleaned, test_original, test_cleaned
    else:
        return train_original, train_cleaned, None, None


def safe_execute(default, exception, function, *args):
    """
    Method to try to execute a function, if it fails return default value
    :param default: value to return when try fails
    :param exception: exception raised by the function
    :param function: function that may raise exception
    :param args: argument of the function
    :return: value of function if it does not raise exception else default value
    """
    try: return function(*args)
    except exception: return default


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
