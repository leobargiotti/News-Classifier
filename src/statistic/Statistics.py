import matplotlib.pyplot as plt
import numpy as np
import texthero as hero
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from yellowbrick.classifier import ClassPredictionError
from yellowbrick.classifier.rocauc import roc_auc


class Statistics:

    def __init__(self, classifier, configFile):
        self.classifier = classifier
        self.classes_array = [self.classifier.classes.get(key) for key in self.classifier.classes]
        self.config_file = configFile
        self.column_text = self.config_file.column_text
        self.column_target = self.config_file.column_target

    # ---------DATASET---------

    def class_distribution(self, data_original, data_cleaned):
        """
        Method to display class distribution statistics
        :param data_original: dataframe before removing duplicates and Nan values
        :param data_cleaned: dataframe after removing duplicates and Nan values
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 7))
        for index in range(2):
            sns.countplot(x=self.column_target, data=data_original if index == 0 else data_cleaned, ax=axes[index])
            axes[index].set_xticklabels(self.classes_array)
            axes[index].tick_params(axis='x', labelrotation=90)
            axes[index].set_title(('Before' if index == 0 else 'After') +
                                  ' removal of tuples with NaN and duplicated values')
        plt.show()

    def calculate_information(self):
        """
        Method to compute information about before and after preprocess:
        first rows, class distribution, duplicates and numbers of row
        :return: list of two strings (information before and after preprocess)
        """
        train_original = self.classifier.train_original
        test_original = self.classifier.test_original
        train_cleaned = self.classifier.train_cleaned
        test_cleaned = self.classifier.test_cleaned

        train_preprocessed = self.classifier.model[0].transform(self.classifier.X_train)
        test_preprocessed = self.classifier.model[0].transform(self.classifier.X_test)

        def print_error_dataset(dataset, error):
            return "There is no " + dataset + " set to calculate " + error + "\n \n"

        def print_first_rows(dataset, X, y=None):
            return "The first rows of " + dataset + f" set are: \n{X[self.column_text].head() if y is None else X.head()} \n \n" + \
                   "The first rows of " + dataset + f" set are: \n{X[self.column_target].head() if y is None else y.head()} \n \n" \
                if X is not None else print_error_dataset(dataset, "first rows")

        def print_class_distribution(dataset, data):
            if data is not None:
                class_distribution = data[self.column_target].value_counts()
                if type(class_distribution.index[0]) is not str:
                    class_distribution.set_axis([class_distribution.index.map(self.classifier.classes)], copy=True)
                return "The class distribution on " + dataset + f" set is \n{class_distribution} \n \n"
            else:
                return print_error_dataset(dataset, "class distribution")

        def print_nan(dataset, data):
            return "The numbers of Nan value on " + dataset + f" set are {data[self.column_text].isna().sum()} \n \n" \
                if data is not None else print_error_dataset(dataset, "Nan value")

        def print_duplicate(dataset, data):
            return "The numbers of duplicate elements on " + dataset \
                   + f" set are {sum(data.duplicated(subset=[self.column_text, self.column_target]))} \n \n" \
                if data is not None else print_error_dataset(dataset, "number of duplicates")

        def print_number_row(dataset, data):
            return f"There are {len(data)} rows in the " + dataset + " set \n \n" \
                if data is not None else print_error_dataset(dataset, "number of rows")

        column0 = "Before Preprocess: \n" + print_first_rows("training", train_original) + \
                  print_first_rows("test", test_original) + print_class_distribution("training", train_original) + \
                  print_class_distribution("test", test_original) + \
                  print_nan("training", train_original) + print_nan("test", test_original) + \
                  print_duplicate("training", train_original) + print_duplicate("test", test_original) + \
                  print_number_row("training", train_original) + print_number_row("test", test_original)

        column1 = "After Preprocess: \n" + print_first_rows("training", train_preprocessed, self.classifier.y_train) + \
                  print_first_rows("test", test_preprocessed, self.classifier.y_test) + \
                  print_class_distribution("training", train_cleaned) + print_class_distribution("test", test_cleaned) + \
                  print_nan("training", train_cleaned) + print_nan("test", test_cleaned) + \
                  print_duplicate("training", train_cleaned) + print_duplicate("test", test_cleaned) + \
                  print_number_row("training", self.classifier.X_train) + print_number_row("test", self.classifier.X_test)
        return column0, column1

    def wordcloud(self, data, data_text):
        """
        Method to display wordcloud of a specific dataframe
        :param data: dataframe
        :param data_text: string (training or test)
        """
        hero.visualization.wordcloud(self.classifier.model[0].transform(data), width=800, height=800,
                                     background_color='black', contour_color='black', colormap='viridis',
                                     return_figure=True)
        plt.title("Wordcloud on " + data_text + " set")
        plt.show()

    def show_top20(self, data, data_text):
        """
        Method to display the 20 most frequent words of a specific dataframe
        :param data: dataframe
        :param data_text: string (training or test)
        """
        NUM_TOP_WORDS = 20
        top_20 = hero.visualization.top_words(self.classifier.model[0].transform(data)).head(NUM_TOP_WORDS)
        top_20.plot.bar(rot=90, title="Top 20 words in " + data_text + " set", figsize=(12, 7))
        plt.show()

    def statistics(self):
        """
        Method to display most relevant words for Multinomial classifier and top words in training and test set
        """
        most_frequent_words_train = hero.top_words(self.classifier.model[0].transform(self.classifier.X_train))[:15]
        most_frequent_words_test = hero.top_words(self.classifier.model[0].transform(self.classifier.X_test))[:15]
        feature_names = self.classifier.model[1].get_feature_names_out()
        str_top10 = ""
        for i, classes in enumerate(self.classes_array):
            top10 = np.argsort(self.classifier.model[2].best_estimator_.feature_log_prob_[i])[-10:]
            str_top10 = str_top10 + "\n" + str(classes).upper() + "\n" + str(" ".join(feature_names[top10]))

        return "The most frequents words in training set are: \n" + str(most_frequent_words_train) + "\n\n" + \
               "The most frequents words in test set are: \n" + str(most_frequent_words_test) + "\n\n" + \
               "The most relevant words for MultinomialNB classifier for each class are: " + str_top10

    # ----------CLASSIFIER------------

    def calculate_metrics(self):
        """
        Method to compute classification report
        :return: string about classification report, training and test accuracy
        """
        y_predict = self.classifier.model.predict(self.classifier.X_test)
        return classification_report(self.classifier.y_test, y_predict, target_names=self.classes_array) + "\n\n" + \
               str(f'Final Training Accuracy: {round(self.classifier.model.score(self.classifier.X_train, self.classifier.y_train),2) * 100}%') + "\n" + \
               str(f'Model Accuracy: {round(self.classifier.model.score(self.classifier.X_test, self.classifier.y_test),2) * 100}%')

    def confusion_matrix(self, title):
        """
        Method to display confusion matrix
        :param title: string
        """
        matrix = ConfusionMatrixDisplay.from_estimator(self.classifier.model, self.classifier.X_test,
                                                       self.classifier.y_test, cmap=plt.cm.Blues,
                                                       display_labels=self.classes_array, xticks_rotation="vertical")
        plt.grid(False)
        matrix.ax_.set_title(title)
        plt.show()

    def roc(self):
        """
        Method to display area under the curve
        """
        visualizer = roc_auc(self.classifier.model, self.classifier.X_train, self.classifier.y_train, is_fitted=True,
                             X_test=self.classifier.X_test, y_test=self.classifier.y_test,
                             encoder=self.classifier.classes, show=False)
        visualizer.name = self.classifier.name
        visualizer.show()

    def class_prediction_error(self):
        """
        Method to display class prediction error
        """
        visualizer = ClassPredictionError(self.classifier.model, encoder=self.classifier.classes, is_fitted=True)
        visualizer.name = self.classifier.name
        visualizer.score(self.classifier.X_test, self.classifier.y_test)
        visualizer.show()
