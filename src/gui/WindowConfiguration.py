import customtkinter
import tkinter.messagebox
from tkinter.filedialog import *
from functools import partial

from configuration.ConfigFile import ConfigFile


class WindowConfiguration(customtkinter.CTk):

    def __init__(self, parentWindow):
        super().__init__()

        self.parentWindow = parentWindow

        self.config_file = ConfigFile()

        self.title("Configuration Settings")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.switch_var = customtkinter.StringVar(value=self.config_file.switch_var)

        # ============ frame_config ============
        self.frame_config = customtkinter.CTkFrame(master=self)
        self.frame_config.grid(row=7, column=4, pady=20, padx=20, sticky="nsew")

        self.text_entry = self.config_file.read_all_attributes_section(self.config_file.config_dataset, self.config_file.keys_dataset)

        # First 2 rows
        self.text_label_path = ["Path Training Set", "Path Test Set"]

        self.text_button = ["Load Training CSV", "Load Test CSV"]

        self.button_load, self.label_path_0, self.label_path_1 = [], [], []

        for index in range(len(self.text_label_path)):
            self.label_path_0.append(customtkinter.CTkLabel(master=self.frame_config,
                                                            text=self.text_label_path[index],
                                                            width=10,
                                                            height=10))
            self.label_path_0[index].grid(row=index, column=0, pady=15, padx=15, sticky="nwe")

            self.label_path_1.append(customtkinter.CTkLabel(master=self.frame_config,
                                                            text="null" if self.text_entry[index] is None else self.text_entry[index],
                                                            width=10,
                                                            height=10))
            self.label_path_1[index].grid(row=index, column=1, pady=15, padx=15, sticky="nwe")

            self.button_load.append(customtkinter.CTkButton(master=self.frame_config,
                                                            text="Load CSV" if index == 0 and self.switch_var.get() == "on" else
                                                            self.text_button[index],
                                                            border_width=2,
                                                            fg_color=None,
                                                            command=partial(self.load_file, index),
                                                            state="disabled" if index == 1 and self.switch_var.get() == "on" else "normal"))
            self.button_load[index].grid(row=index, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # Switch test_size/path_test

        switch_test = customtkinter.CTkSwitch(master=self.frame_config, text="", command=self.switch_event,
                                              variable=self.switch_var, onvalue="on", offvalue="off")
        switch_test.grid(row=2, column=2, pady=10, padx=10)

        # Other rows

        self.text_label = ["Test/Training size", "Column Text", "Column Target",
                           "Language", "Class Target is a String", "Integer number \n of each class",
                           "Name of classes \n respective of number of labels"]

        self.entry, self.label = [], []

        for index in range(len(self.text_label)):
            self.label.append(customtkinter.CTkLabel(master=self.frame_config,
                                                     text=self.text_label[index],
                                                     width=10,
                                                     height=10))
            self.label[index].grid(row=index + 2, column=0, pady=15, padx=15, sticky="nwe")
            self.entry.append(customtkinter.CTkEntry(master=self.frame_config,
                                                     height=10,
                                                     corner_radius=6,
                                                     justify=tkinter.LEFT,
                                                     placeholder_text="" if index == 0 and self.switch_var.get() == "off" else
                                                     str(self.text_entry[index + 2]),
                                                     fg_color=('gray38', 'white')
                                                     if index == 0 and self.switch_var.get() == "off" else
                                                     ('white', 'gray38'),
                                                     state="disabled" if index == 0 and self.switch_var.get() == "off" else "normal"))
            self.entry[index].grid(column=1, row=index + 2, sticky="nwe", padx=15, pady=15)

        self.text_button_config = ["Default Configuration", "Save"]

        self.button_event_config = [self.button_event_reset, self.button_event_save]

        self.buttons_config = []

        for index in range(len(self.text_button_config)):
            self.buttons_config.append(customtkinter.CTkButton(master=self.frame_config,
                                                               text=self.text_button_config[index],
                                                               border_width=2,
                                                               fg_color=None,
                                                               command=self.button_event_config[index]))
            self.buttons_config[index].grid(row=9, column=index, columnspan=1, pady=20, padx=20, sticky="we")

        # ------------PREPROCESS---------------

        label = customtkinter.CTkLabel(master=self.frame_config, text="Preprocessing:")
        label.grid(row=0, column=3, pady=10, padx=10)

        text_checkbox = ["Stopwords", "Stemming", "Lemmatization", "Digits", "Expanding Contractions", "Urls",
                         "Html Tags", "Punctuation", "Diacritics", "Lowercase", "Extra Whitespace", "Use Idf"]
        self.n_checkbox = len(text_checkbox)
        self.check_var = [customtkinter.StringVar(value=str(att)) for att in
                          self.config_file.read_all_attributes_section(self.config_file.config_preprocess, self.config_file.keys_preprocess)][:self.n_checkbox]

        checkbox = []

        for index in range(len(self.check_var)):
            checkbox.append(customtkinter.CTkCheckBox(master=self.frame_config, text=text_checkbox[index],
                                                      variable=self.check_var[index], onvalue="True", offvalue="False"))
            checkbox[index].grid(row=1+index if index < int(self.n_checkbox/2) else 1+index-int(self.n_checkbox/2),
                                 column=3 if index < int(self.n_checkbox/2) else 4, pady=10, padx=10)

        text_entry = [att for att in self.config_file.read_all_attributes_section(
            self.config_file.config_preprocess, self.config_file.keys_preprocess)][self.n_checkbox:]

        text_label_preprocessing = ["N_Grams", "Max_df", "Min_df"]
        self.entry_tfidf, label = [], []

        for index in range(len(text_label_preprocessing)):
            label.append(customtkinter.CTkLabel(master=self.frame_config, text=text_label_preprocessing[index]))
            label[index].grid(row=int(self.n_checkbox/2)+1+index, column=3, pady=10, padx=10)
            self.entry_tfidf.append(customtkinter.CTkEntry(master=self.frame_config, placeholder_text=text_entry[index], height=10,
                                                     corner_radius=6, fg_color=('white', "gray38")))
            self.entry_tfidf[index].grid(row=int(self.n_checkbox/2)+1+index, column=4, pady=10, padx=10)

    def load_file(self, index):
        """
        Method to load file
        :param index: integer value of index of label_path_1 array
        """
        self.text_entry[index] = askopenfilenames()[0]
        self.label_path_1[index].configure(text=self.text_entry[index])

    def switch_event(self):
        """
        Method to change parameters of window depending on switch value
        """
        self.entry[0].configure(state="disabled" if self.switch_var.get() == "off" else "normal",
                                fg_color=('gray38', 'white') if self.switch_var.get() == "off" else ('white', 'gray38'),
                                placeholder_text=" " if self.switch_var.get() == "off" else self.text_entry[2])
        self.label_path_1[1].configure(text=self.text_entry[1] if self.switch_var.get() == "off" else "null",
                                       state="disabled" if self.switch_var.get() == "on" else "normal")
        self.button_load[0].configure(text="Load CSV" if self.switch_var.get() == "on" else self.text_button[0])
        self.button_load[1].configure(state="disabled" if self.switch_var.get() == "on" else "normal")

    def button_event_save(self):
        """
        Method to save configuration
        """
        modification_config = False
        for index in range(len(self.entry)+2):
            text_to_check = self.label_path_1[index].cget("text") if index < 2 else self.entry[index - 2].get()
            if not text_to_check == self.config_file.read_attribute(
                    self.config_file.config_dataset, self.config_file.keys_dataset[index]) and text_to_check != "":
                self.config_file.update_config_file(self.config_file.config_dataset, self.config_file.keys_dataset[index], text_to_check)
                modification_config = True
        self.config_file.update_config_file(self.config_file.config_configuration, self.config_file.key_switch_var, self.switch_var.get())
        for index in range(len(self.check_var)):
            if not self.check_var[index].get() == self.config_file.read_attribute(
                    self.config_file.config_preprocess, self.config_file.keys_preprocess[index]):
                self.config_file.update_config_file(self.config_file.config_preprocess, self.config_file.keys_preprocess[index], self.check_var[index].get())
                modification_config = True
        for index in range(len(self.entry_tfidf)):
            if self.entry_tfidf[index].get() != "" and self.entry_tfidf[index].get() != self.config_file.read_attribute(
                    self.config_file.config_preprocess, self.config_file.keys_preprocess[self.n_checkbox+index]):
                self.config_file.update_config_file(self.config_file.config_preprocess, self.config_file.keys_preprocess[self.n_checkbox+index], self.entry_tfidf[index].get())
                modification_config = True
        if modification_config: self.parentWindow.reload_config_classifier()
        self.on_closing()

    def button_event_reset(self):
        """
        Method to write default configuration
        """
        self.config_file.create_default_config_file()
        for index in range(len(self.text_entry)):
            if index > 1: self.entry[index - 2].configure(placeholder_text=self.config_file.dataset_default[index])
            else: self.label_path_1[index].configure(text=self.config_file.dataset_default[index])
        self.switch_var.set(self.config_file.switch_var_default)
        self.switch_event()
        for index in range(len(self.check_var)): self.check_var[index].set(self.config_file.preprocess_default[index])
        for index in range(len(self.entry_tfidf)): self.entry_tfidf[index].configure(placeholder_text=self.config_file.preprocess_default[self.n_checkbox+index])
        self.parentWindow.reload_config_classifier()

    def on_closing(self):
        """
        Method to close window
        """
        self.parentWindow.windows[0] = None
        self.destroy()
