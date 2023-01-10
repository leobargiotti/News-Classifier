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
        self.frame_config.grid(row=7, column=2, pady=20, padx=20, sticky="nsew")

        self.text_entry = [self.config_file.dictionary[key] for key in self.config_file.dictionary]

        # First 2 rows

        self.label_path = ["label_train", "label_test"]

        self.text_label_path = ["Path Training Set", "Path Test Set"]

        self.text_button = ["Load Training CSV", "Load Test CSV"]

        self.button_load = ["self.button_train", "self.button_test"]

        for index in range(len(self.label_path)):
            self.label_path[index] = customtkinter.CTkLabel(master=self.frame_config,
                                                            text=self.text_label_path[index],
                                                            width=10,
                                                            height=10)
            self.label_path[index].grid(row=index, column=0, pady=15, padx=15, sticky="nwe")

            self.label_path[index] = customtkinter.CTkLabel(master=self.frame_config,
                                                            text=self.text_entry[index],
                                                            width=10,
                                                            height=10)
            self.label_path[index].grid(row=index, column=1, pady=15, padx=15, sticky="nwe")

            self.button_load[index] = customtkinter.CTkButton(master=self.frame_config,
                                                              text="Load CSV" if index == 0 and self.switch_var.get() == "on" else self.text_button[index],
                                                              border_width=2,
                                                              fg_color=None,
                                                              command=partial(self.load_file, index),
                                                              state="disabled" if index == 1 and self.switch_var.get() == "on" else "normal")
            self.button_load[index].grid(row=index, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # Switch test_size/path_test

        switch_test = customtkinter.CTkSwitch(master=self.frame_config, text="", command=self.switch_event,
                                              variable=self.switch_var, onvalue="on", offvalue="off")
        switch_test.grid(row=2, column=2, pady=10, padx=10)

        # Other rows

        self.name_config = [key for key in self.config_file.dictionary]

        self.label = ["label_test_size", "label_column_text", "label_column_target",
                      "label_language", "label_boolean_class", "label_int_classes", "label_name_classes"]

        self.text_label = ["Test/Training size", "Column Text", "Column Target",
                           "Language", "Class Target is a String", "Integer number \n of each class",
                           "Name of classes \n respective of number of labels"]

        self.entry = ["entry_test_size", "entry_column_text", "entry_column_target",
                      "entry_language", "entry_boolean_class", "entry_int_classes", "entry_name_classes"]

        for index in range(len(self.label)):
            self.label[index] = customtkinter.CTkLabel(master=self.frame_config,
                                                       text=self.text_label[index],
                                                       width=10,
                                                       height=10)
            self.label[index].grid(row=index + 2, column=0, pady=15, padx=15, sticky="nwe")

            self.entry[index] = customtkinter.CTkEntry(master=self.frame_config,
                                                       height=10,
                                                       corner_radius=6,  # <- custom corner radius
                                                       justify=tkinter.LEFT,
                                                       placeholder_text="" if index == 0 and self.switch_var.get() == "off" else self.text_entry[index + 2],
                                                       fg_color=('gray38', 'white') if index == 0 and self.switch_var.get() == "off" else ('white', 'gray38'),
                                                       state="disabled" if index == 0 and self.switch_var.get() == "off" else "normal")
            self.entry[index].grid(column=1, row=index + 2, sticky="nwe", padx=15, pady=15)

        # ============ frame_right ============
        self.button_save = customtkinter.CTkButton(master=self.frame_config,
                                                   text="Save",
                                                   border_width=2,
                                                   fg_color=None,
                                                   command=self.button_event_save)
        self.button_save.grid(row=9, column=1, pady=20, padx=20, sticky="we")

        self.button_reset = customtkinter.CTkButton(master=self.frame_config,
                                                    text="Default Configuration",
                                                    border_width=2,
                                                    fg_color=None,
                                                    command=self.button_event_reset)
        self.button_reset.grid(row=9, column=0, pady=20, padx=20, sticky="we")

    def load_file(self, index):
        """
        Method to load training file
        """
        self.text_entry[index] = askopenfilenames()[0]
        self.label_path[index].configure(text=self.text_entry[index])

    def switch_event(self):
        """
        Method to change parameters of window depending on switch value
        """
        self.entry[0].configure(state="disabled" if self.switch_var.get() == "off" else "normal",
                                fg_color=('gray38', 'white') if self.switch_var.get() == "off" else ('white', 'gray38'),
                                placeholder_text=" " if self.switch_var.get() == "off" else self.text_entry[2])
        self.label_path[1].configure(text=self.text_entry[1] if self.switch_var.get() == "off" else "null",
                                     state="disabled" if self.switch_var.get() == "on" else "normal")
        self.button_load[0].configure(text="Load CSV" if self.switch_var.get() == "on" else self.text_button[0])
        self.button_load[1].configure(state="disabled" if self.switch_var.get() == "on" else "normal")

    def button_event_save(self):
        """
        Method to save configuration
        """
        modification_config = False
        for index in range(len(self.entry)):
            text_to_check = self.label_path[index].cget("text") if index < 2 else self.entry[index-2].get()
            if not text_to_check == self.config_file.read_attribute(self.config_file.config_file_dataset, self.name_config[index]) and text_to_check != "":
                self.config_file.update_config_file(self.config_file.config_file_dataset, self.name_config[index], text_to_check)
                modification_config = True
        self.config_file.update_config_file(self.config_file.config_file_config, self.config_file.key_config, self.switch_var.get())
        if modification_config: self.parentWindow.reload_config_classifier()
        self.destroy()

    def button_event_reset(self):
        """
        Method to write default configuration
        """
        self.config_file.create_default_config_file()
        self.config_file.dictionary = self.config_file.create_dictionary_config_file(self.config_file.default_values)
        self.text_entry = [self.config_file.dictionary[key] for key in self.config_file.dictionary]
        for index in range(len(self.text_entry)):
            if index > 1:
                self.entry[index-2].configure(placeholder_text=self.text_entry[index])
            else:
                self.label_path[index].configure(text=self.text_entry[index])
        self.switch_var.set(self.config_file.switch_var_default)
        self.switch_event()
        self.parentWindow.reload_config_classifier()

    def on_closing(self):
        """
        Method to close window
        """
        self.destroy()
