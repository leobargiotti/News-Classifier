import customtkinter
import tkinter.messagebox

from statistic.Statistics import Statistics


class WindowStatistics(customtkinter.CTk):

    def __init__(self, parentWindow):
        super().__init__()

        self.parentWindow = parentWindow

        self.statistic_classifiers = [Statistics(classifier, classifier.config_file) for classifier in
                                      self.parentWindow.classifiers]

        self.title("Statistics")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ============ frame_info ============
        self.frame_statistics = customtkinter.CTkFrame(master=self)
        self.frame_statistics.grid(row=11, column=2, pady=20, padx=20, sticky="nsew")

        # ============ Button Dataset ============
        self.button_dataset = ["button_class_distribution_train", "button_class_distribution_test",
                               "button_information", "button_wordcloud_train", "button_wordcloud_test",
                               "button_statistics", "button_top20_train", "button_top20_test"]

        self.text_dataset = ["Class Distribution Training Set", "Class Distribution Test Set",
                             "Information on Dataset", "WordCloud on Training Set", "WordCloud on Test Set",
                             "Statistics on words in Dataset", "Top 20 Words in Training Set",
                             "Top 20 Words in Test Set"]

        self.button_event_dataset = [self.button_event_class_distribution_train,
                                     self.button_event_class_distribution_test,
                                     self.button_event_information, self.button_event_wordcloud_train,
                                     self.button_event_wordcloud_test, self.button_event_statistics,
                                     self.button_event_top20_train, self.button_event_top20_test]

        self.label_dataset = customtkinter.CTkLabel(master=self.frame_statistics,
                                                    text="Statistics on Dataset:",
                                                    font=("Roboto Medium", -15))
        self.label_dataset.grid(row=0, column=0, pady=10, padx=10)

        for index in range(len(self.button_dataset)):
            self.button_dataset[index] = customtkinter.CTkButton(master=self.frame_statistics,
                                                                 text=self.text_dataset[index],
                                                                 border_width=2,
                                                                 fg_color=None,
                                                                 command=self.button_event_dataset[index])
            self.button_dataset[index].grid(row=1 + int(index / 3), column=index % 3, pady=20, padx=20, sticky="we")

        self.button_dataset[1].configure(
            state="normal" if self.statistic_classifiers[0].classifier.test_cleaned is not None else "disabled")

        self.button_dataset[0].configure(
            text="Class Distribution Dataset" if self.statistic_classifiers[0].classifier.test_cleaned is None else
            self.text_dataset[0])
        # ============ Button Classifiers ============

        self.button_classifier = ["button_metrics_1", "button_metrics_2", "button_metrics_3",
                                  "button_cm_1", "button_cm_2", "button_cm_3",
                                  "button_roc_1", "button_roc_2", "button_roc_3", "button_class_predict_error_1",
                                  "button_class_predict_error_2", "button_class_predict_error_3"]

        self.text_classifier = ["Classification Report Config.1", "Classification Report Config.2",
                                "Classification Report Config.3",
                                "Confusion Matrix Config. 1", " Confusion Matrix Config. 2",
                                "Confusion Matrix Config. 3", "AUC Config.1", "AUC Config.2", "AUC Config.3",
                                "Class Predict. Error Config. 1", "Class Predict. Error Config. 2",
                                "Class Predict. Error Config. 3"]

        self.button_event_classifier = [self.button_event_metrics_1, self.button_event_metrics_2,
                                        self.button_event_metrics_3, self.button_event_cm1, self.button_event_cm2,
                                        self.button_event_cm3, self.button_event_roc_1, self.button_event_roc_2,
                                        self.button_event_roc_3, self.button_event_class_predict_error_1,
                                        self.button_event_class_predict_error_2,
                                        self.button_event_class_predict_error_3]

        self.label_dataset = customtkinter.CTkLabel(master=self.frame_statistics,
                                                    text="Statistics on Classifiers:",
                                                    font=("Roboto Medium", -15))
        self.label_dataset.grid(row=8, column=0, pady=10, padx=10)

        for index in range(len(self.button_classifier)):
            self.button_classifier[index] = customtkinter.CTkButton(master=self.frame_statistics,
                                                                    text=self.text_classifier[index],
                                                                    border_width=2,
                                                                    fg_color=None,
                                                                    command=self.button_event_classifier[index])
            self.button_classifier[index].grid(row=9 + int(index / 3), column=index % 3, pady=20, padx=20, sticky="we")

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
        window.label_1 = customtkinter.CTkLabel(master=window.frame, text=column0, justify=tkinter.LEFT, font=("Courier", 14))
        window.label_1.grid(row=0, column=0, pady=10, padx=10)
        window.label_1 = customtkinter.CTkLabel(master=window.frame, text=column1, justify=tkinter.LEFT, font=("Courier", 14))
        window.label_1.grid(row=0, column=1, pady=10, padx=10)

    # DATASET

    def button_event_class_distribution_train(self):
        """
        Method to display class distribution statistic of training set
        """
        self.statistic_classifiers[0].class_distribution(self.statistic_classifiers[0].classifier.train_original,
                                                         self.statistic_classifiers[0].classifier.train_cleaned)

    def button_event_class_distribution_test(self):
        """
        Method to display class distribution statistic of test set
        """
        self.statistic_classifiers[0].class_distribution(self.statistic_classifiers[0].classifier.test_original,
                                                         self.statistic_classifiers[0].classifier.test_cleaned)

    def button_event_information(self):
        """
        Method to display information on dataset
        """
        column0, column1 = self.statistic_classifiers[0].calculate_information()
        self.create_toplevel_information(column0, column1)

    def button_event_wordcloud_train(self):
        """
        Method to display wordcloud of training set
        """
        self.statistic_classifiers[0].wordcloud(self.statistic_classifiers[0].classifier.X_train, "training")

    def button_event_wordcloud_test(self):
        """
        Method to display wordcloud of test set
        """
        self.statistic_classifiers[0].wordcloud(self.statistic_classifiers[0].classifier.X_test, "test")

    def button_event_top20_train(self):
        """
        Method to display 20 most frequent words of training set
        """
        self.statistic_classifiers[0].show_top20(self.statistic_classifiers[0].classifier.X_train, "training")

    def button_event_top20_test(self):
        """
        Method to display 20 most frequent words of test set
        """
        self.statistic_classifiers[0].show_top20(self.statistic_classifiers[0].classifier.X_test, "test")

    def button_event_statistics(self):
        """
        Method to display same statistics on dataset
        """
        self.create_toplevel(self.statistic_classifiers[0].statistics(), "Statistics on words in Dataset")

    # CLASSIFIER

    def button_event_metrics_1(self):
        """
        Method to display classification report of classifierTfidfMultinomialNB
        """
        self.create_toplevel(self.statistic_classifiers[0].calculate_metrics(), "Classification Report Configuration 1")

    def button_event_metrics_2(self):
        """
        Method to display classification report of classifierTfidfLogReg
        """
        self.create_toplevel(self.statistic_classifiers[1].calculate_metrics(), "Classification Report Metrics Configuration 2")

    def button_event_metrics_3(self):
        """
        Method to display classification report of classifierTfidfSGD
        """
        self.create_toplevel(self.statistic_classifiers[2].calculate_metrics(), "Classification Report Metrics Configuration 3")

    def button_event_cm1(self):
        """
        Method to display confusion matrix of classifierTfidfMultinomialNB
        """
        self.statistic_classifiers[0].confusion_matrix("Confusion Matrix Config. 1")

    def button_event_cm2(self):
        """
        Method to display confusion matrix of classifierTfidfLogReg
        """
        self.statistic_classifiers[1].confusion_matrix("Confusion Matrix Config. 2")

    def button_event_cm3(self):
        """
        Method to display confusion matrix of classifierTfidfSGD
        """
        self.statistic_classifiers[2].confusion_matrix("Confusion Matrix Config. 3")

    def button_event_roc_1(self):
        """
        Method to display area under the curve of classifierTfidfMultinomialNB
        """
        self.statistic_classifiers[0].roc()

    def button_event_roc_2(self):
        """
        Method to display area under the curve of classifierTfidfLogReg
        """
        self.statistic_classifiers[1].roc()

    def button_event_roc_3(self):
        """
        Method to display area under the curve of classifierTfidfSGD
        """
        self.statistic_classifiers[2].roc()

    def button_event_class_predict_error_1(self):
        """
        Method to display class prediction error of classifierTfidfMultinomialNB
        """
        self.statistic_classifiers[0].class_prediction_error()

    def button_event_class_predict_error_2(self):
        """
        Method to display class prediction error of classifierTfidfLogReg
        """
        self.statistic_classifiers[1].class_prediction_error()

    def button_event_class_predict_error_3(self):
        """
        Method to display class prediction error of classifierTfidfSGD
        """
        self.statistic_classifiers[2].class_prediction_error()

    def on_closing(self):
        """
        Method to close window
        """
        self.destroy()
