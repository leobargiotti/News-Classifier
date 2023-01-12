import customtkinter
import tkinter.messagebox
from tkinter.filedialog import *
import pandas as pd
import numpy as np
from tqdm import tqdm


class WindowTest(customtkinter.CTk):

    def __init__(self, parentWindow):
        super().__init__()

        self.parentWindow = parentWindow

        self.title("Test Models")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ============ frame_test ============
        self.frame_test = customtkinter.CTkFrame(master=self)
        self.frame_test.grid(row=7, column=2, pady=20, padx=20, sticky="nsew")

        self.button_load_csv = customtkinter.CTkButton(master=self.frame_test,
                                                       text="Load CSV",
                                                       border_width=2,
                                                       fg_color=None,
                                                       command=self.button_event_load_csv)
        self.button_load_csv.grid(row=0, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        self.button_classify_csv = customtkinter.CTkButton(master=self.frame_test,
                                                           text="Classify CSV",
                                                           border_width=2,
                                                           fg_color=None,
                                                           command=self.button_event_classify)
        self.button_classify_csv.grid(row=9, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        self.label_load_csv = customtkinter.CTkLabel(master=self.frame_test,
                                                     text="Path CSV",
                                                     width=10,
                                                     height=10)
        self.label_load_csv.grid(row=0, column=0, pady=15, padx=15, sticky="nwe")

        self.label_loaded_csv = customtkinter.CTkLabel(master=self.frame_test,
                                                       text="null",
                                                       width=10,
                                                       height=10)
        self.label_loaded_csv.grid(row=0, column=1, pady=15, padx=15, sticky="nwe")

        self.label_text_classes = list(classes for classes in self.parentWindow.classifiers[0].classes.values())

        self.label_text = ["Column Text", "Column Classes"] + self.label_text_classes

        self.label, self.entry = [], []

        for index in range(len(self.label_text)):
            self.label.append(customtkinter.CTkLabel(master=self.frame_test,
                                                     text=self.label_text[index],
                                                     width=10,
                                                     height=10))
            self.label[index].grid(row=index + 1, column=0, pady=15, padx=15, sticky="nwe")
            self.entry.append(customtkinter.CTkEntry(master=self.frame_test,
                                                     height=10,
                                                     corner_radius=6,
                                                     justify=tkinter.LEFT,
                                                     placeholder_text="",
                                                     fg_color=('white', 'gray38')))
            self.entry[index].grid(column=1, row=index + 1, sticky="nwe", padx=15, pady=15)

    def button_event_load_csv(self):
        """
        Method to save path of csv
        """
        self.label_loaded_csv.configure(text=askopenfilenames()[0])

    def button_event_classify(self):
        """
        Method to launch classification
        """
        self.classify(self.label_loaded_csv.cget("text"),
                      self.entry[0].get(), self.entry[1].get(),
                      dict(zip(self.label_text_classes, [i.get() for i in self.entry[2:]])))

    def classify(self, path_csv, column_text, column_class, dict_classes):
        """
        Method to compute classification of csv in input creating new file containing the same columns
        of file in input and other three for each classifier:class predicted, its probability and
        boolean value (0 or 1) if the class predicted is or isn't the same of the right class
        When te classification is finished it opens a pop-up window and displays accuracy of each classifier
        :param path_csv: string containing path of csv file
        :param column_text: string column name containing text
        :param column_class: string column name containing classes
        :param dict_classes: dictionary of relationship between classes of classifier and csv file
        """
        df_test = pd.read_csv(path_csv)
        for index, row in tqdm(df_test.iterrows(), total=len(df_test), desc="Processing Rows"):
            for classifier in self.parentWindow.classifiers:
                class_predicted = classifier.print_class(classifier.model.predict(pd.Series(row[column_text]))[0])
                class_predicted_probability = classifier.model.predict_proba(pd.Series(row[column_text]))
                df_test.at[index, "ClassPredicted" + classifier.name[15:]] = class_predicted
                df_test.at[index, "Probability" + classifier.name[15:]] = round(class_predicted_probability[0][np.argmax(class_predicted_probability)], 2)
                df_test.at[index, "Correctness" + classifier.name[15:]] = 1 if str(df_test.at[index, column_class]) not in dict_classes[class_predicted] else 0
        df_test.to_csv(path_csv[:-4] + "_predictions" + path_csv[-4:], index=False, mode='w+')
        accuracy = [classifier.name[15:] + ": " + "%.2f" % ((1 - round(sum(df_test["Correctness" + classifier.name[15:]]) / len(df_test), 4)) * 100) + "%\n"
                    for classifier in self.parentWindow.classifiers]
        tkinter.messagebox.showinfo('News Classifier', 'The operation is concluded\n Accuracy:\n' + "".join(accuracy))

    def on_closing(self):
        """
        Method to close window
        """
        self.parentWindow.windowTest = None
        self.destroy()
