import customtkinter
import tkinter.messagebox
from functools import partial

from statistic.Statistics import Statistics


class WindowStatistics(customtkinter.CTk):

    def __init__(self, parentWindow):
        super().__init__()

        self.parentWindow = parentWindow

        self.statistic_classifiers = [Statistics(classifier, classifier.config_file) for classifier in
                                      self.parentWindow.classifiers]

        self.number_classifiers = len(self.statistic_classifiers)

        self.title("Statistics")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ============ frame_statistics ============
        self.frame_statistics = customtkinter.CTkFrame(master=self)
        self.frame_statistics.grid(row=11, column=2, pady=20, padx=20, sticky="nsew")

        # ============ Button Dataset ============
        self.button_dataset = []

        self.text_dataset = ["Class Distribution Training Set", "Class Distribution Test Set",
                             "Information on Dataset", "WordCloud on Training Set", "WordCloud on Test Set",
                             "Statistics on words in Dataset", "Top 20 Words in Training Set",
                             "Top 20 Words in Test Set"]

        self.button_event_dataset = [partial(self.button_event_class_distribution, "train_original", "train_cleaned"),
                                     partial(self.button_event_class_distribution, "test_original", "test_cleaned"),
                                     self.button_event_information, partial(self.button_event_wordcloud, "X_train", "training"),
                                     partial(self.button_event_wordcloud, "X_test", "test"), self.button_event_statistics,
                                     partial(self.button_event_top20, "X_train", "training"),
                                     partial(self.button_event_top20, "X_test", "test")]

        self.label_dataset = customtkinter.CTkLabel(master=self.frame_statistics,
                                                    text="Statistics on Dataset:",
                                                    font=("Roboto Medium", -15))
        self.label_dataset.grid(row=0, column=0, pady=10, padx=10)

        for index in range(len(self.text_dataset)):
            self.button_dataset.append(customtkinter.CTkButton(master=self.frame_statistics,
                                                               text=self.text_dataset[index],
                                                               border_width=2,
                                                               fg_color=None,
                                                               command=self.button_event_dataset[index]))
            self.button_dataset[index].grid(row=1 + int(index / 3), column=index % 3, pady=20, padx=20, sticky="we")

        self.button_dataset[1].configure(
            state="normal" if self.statistic_classifiers[0].classifier.test_cleaned is not None else "disabled")

        self.button_dataset[0].configure(
            text="Class Distribution Dataset" if self.statistic_classifiers[0].classifier.test_cleaned is None else
            self.text_dataset[0])

        # ============ Button Classifiers ============
        self.button_classifier = []

        self.text_classifier = self.print_string_with_number_config("Classification Report Config. ") + \
                               self.print_string_with_number_config("Confusion Matrix Config. ") + \
                               self.print_string_with_number_config("AUC Config. ") + \
                               self.print_string_with_number_config("Class Predict. Error Config. ")

        self.button_event_classifier = [self.button_event_class_report, self.button_event_conf_matrix,
                                        self.button_event_roc, self.button_event_class_predict_error]

        self.label_dataset = customtkinter.CTkLabel(master=self.frame_statistics,
                                                    text="Statistics on Classifiers:",
                                                    font=("Roboto Medium", -15))
        self.label_dataset.grid(row=8, column=0, pady=10, padx=10)

        for index in range(len(self.text_classifier)):
            self.button_classifier.append(customtkinter.CTkButton(master=self.frame_statistics,
                                                                  text=self.text_classifier[index],
                                                                  border_width=2,
                                                                  fg_color=None,
                                                                  command=partial(self.button_event_classifier[
                                                                                      int(index / self.number_classifiers)],
                                                                                  index % self.number_classifiers)))
            self.button_classifier[index].grid(row=9 + int(index / self.number_classifiers),
                                               column=index % self.number_classifiers, pady=20, padx=20, sticky="we")

    def print_string_with_number_config(self, string):
        """
        Method to concatenate string to index+1 of statistic_classifiers
        :param string: string name of statist
        :return: array concatenate string to index+1
        """
        return [string + str(index + 1) for index in range(len(self.statistic_classifiers))]

    def create_toplevel(self, metrics, title):
        """
        Method to create toplevel windows for statistics
        :param metrics: body of the new window (statistic)
        :param title: string title of the statistic
        """
        window = customtkinter.CTkToplevel(self)
        window.title(title)
        window.frame = customtkinter.CTkFrame(master=window)
        window.frame.grid(pady=20, padx=20, sticky="nsew")
        label = customtkinter.CTkLabel(master=window.frame, text=metrics, justify=tkinter.LEFT, font=("Courier", 14))
        label.pack(side="top", fill="both", expand=True, padx=20, pady=20)

    def create_toplevel_information(self, column0, column1):
        """
        Method to create toplevel windows for statistics
        :param column0: string containing information to display
        :param column1: string containing information to display
        """
        window = customtkinter.CTkToplevel(self)
        window.title("Information on Dataset")
        window.frame = customtkinter.CTkFrame(master=window)
        window.frame.grid(row=1, column=2, pady=20, padx=20, sticky="nsew")
        window.label_1 = customtkinter.CTkLabel(master=window.frame, text=column0, justify=tkinter.LEFT,
                                                font=("Courier", 14))
        window.label_1.grid(row=0, column=0, pady=10, padx=10)
        window.label_1 = customtkinter.CTkLabel(master=window.frame, text=column1, justify=tkinter.LEFT,
                                                font=("Courier", 14))
        window.label_1.grid(row=0, column=1, pady=10, padx=10)

    # DATASET

    def button_event_class_distribution(self, data_original, data_cleaned):
        """
        Method to display class distribution statistic of training set
        :param data_original: dataframe with duplicates and nan values
        :param data_cleaned: dataframe without duplicates and nan values
        """
        self.statistic_classifiers[0].class_distribution(getattr(self.statistic_classifiers[0].classifier, data_original),
                                                         getattr(self.statistic_classifiers[0].classifier, data_cleaned))

    def button_event_information(self):
        """
        Method to display information on dataset
        """
        column0, column1 = self.statistic_classifiers[0].calculate_information()
        self.create_toplevel_information(column0, column1)

    def button_event_wordcloud(self, data, data_title):
        """
        Method to display wordcloud
        :param data: dataframe on which calculate wordcloud
        :param data_title: string on title of wordcloud (training or test)
        """
        self.statistic_classifiers[0].wordcloud(getattr(self.statistic_classifiers[0].classifier, data), data_title)

    def button_event_statistics(self):
        """
        Method to display same statistics on dataset
        """
        self.create_toplevel(self.statistic_classifiers[0].statistics(), "Statistics on words in Dataset")

    def button_event_top20(self, data, data_title):
        """
        Method to display 20 most frequent words
        :param data: dataframe on which calculate most frequent words
        :param data_title: string on title of wordcloud (training or test)
        """
        self.statistic_classifiers[0].show_top20(getattr(self.statistic_classifiers[0].classifier, data), data_title)

    # CLASSIFIER

    def button_event_class_report(self, index):
        """
        Method to display classification report of classifier in position of index
        :param index: integer value of index corresponding to the classifier
        """
        self.create_toplevel(self.statistic_classifiers[index].calculate_class_report(),
                             "Classification Report Configuration " + str(index + 1))

    def button_event_conf_matrix(self, index):
        """
        Method to display confusion matrix of classifier in position of index
        :param index: integer value of index corresponding to the classifier
        """
        self.statistic_classifiers[index].confusion_matrix("Confusion Matrix Config. " + str(index + 1))

    def button_event_roc(self, index):
        """
        Method to display area under the curve of classifier in position of index
        :param index: integer value of index corresponding to the classifier
        """
        self.statistic_classifiers[index].roc()

    def button_event_class_predict_error(self, index):
        """
        Method to display class prediction error of classifier in position of index
        :param index: integer value of index corresponding to the classifier
        """
        self.statistic_classifiers[index].class_prediction_error()

    def on_closing(self):
        """
        Method to close window
        """
        self.parentWindow.windowStats = None
        self.destroy()
