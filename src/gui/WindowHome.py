import tkinter.messagebox
import customtkinter

from .WindowConfiguration import WindowConfiguration
from .WindowStatistics import WindowStatistics
from .WindowTest import WindowTest
from classifier.ClassifierTfidfMultinomialNB import ClassifierTfidfMultinomialNB
from classifier.ClassifierTfidfLogReg import ClassifierTfidfLogReg
from classifier.ClassifierTfidfSGD import ClassifierTfidfSGD

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"


class WindowHome(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("News Classifier")
        self.geometry(f"{WindowHome.WIDTH}x{WindowHome.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.classifierTfidfMultinomialNB = ClassifierTfidfMultinomialNB()
        self.classifierTfidfLogReg = ClassifierTfidfLogReg()
        self.classifierTfidfSGD = ClassifierTfidfSGD()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_buttons = customtkinter.CTkFrame(master=self,
                                                    width=180,
                                                    corner_radius=0)
        self.frame_buttons.grid(row=0, column=0, sticky="nswe")

        self.frame_button_classify = customtkinter.CTkFrame(master=self)
        self.frame_button_classify.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_buttons ============

        self.frame_buttons.grid_rowconfigure(0, minsize=10)
        self.frame_buttons.grid_rowconfigure(5, weight=1)
        self.frame_buttons.grid_rowconfigure(8, minsize=20)
        self.frame_buttons.grid_rowconfigure(11, minsize=10)

        # configure grid layout (1x11)
        self.label_settings = customtkinter.CTkLabel(master=self.frame_buttons,
                                                     text="News Classifier",
                                                     font=("Roboto Medium", -16))  # font name and size in px
        self.label_settings.grid(row=1, column=0, pady=10, padx=10)

        self.button_config = customtkinter.CTkButton(master=self.frame_buttons,
                                                     text="Configuration Settings",
                                                     border_width=2,
                                                     fg_color=None,
                                                     command=self.button_event_config)
        self.button_config.grid(row=2, column=0, columnspan=1, pady=20, padx=20, sticky="we")

        self.button_statistics = customtkinter.CTkButton(master=self.frame_buttons,
                                                         text="Statistics",
                                                         border_width=2,
                                                         fg_color=None,
                                                         command=self.button_event_statistics)
        self.button_statistics.grid(row=3, column=0, columnspan=1, pady=20, padx=20, sticky="we")

        self.button_statistics = customtkinter.CTkButton(master=self.frame_buttons,
                                                         text="Test Models",
                                                         border_width=2,
                                                         fg_color=None,
                                                         command=self.button_event_test)
        self.button_statistics.grid(row=4, column=0, columnspan=1, pady=20, padx=20, sticky="we")

        self.label_appearance = customtkinter.CTkLabel(master=self.frame_buttons, text="Appearance Mode:")
        self.label_appearance.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.menu_appearance = customtkinter.CTkOptionMenu(master=self.frame_buttons,
                                                           values=["Light", "Dark", "System"],
                                                           command=self.change_appearance_mode)
        self.menu_appearance.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_button_classify.rowconfigure(10, weight=10)
        self.frame_button_classify.columnconfigure(0, weight=1)

        self.frame_home = customtkinter.CTkFrame(master=self.frame_button_classify)
        self.frame_home.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_home.columnconfigure(1, weight=1)

        self.text_input = customtkinter.CTkTextbox(master=self.frame_home,
                                                   height=130,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"))

        self.text_input.grid(column=0, row=0, columnspan=2, sticky="nwe", padx=15, pady=15)

        self.label = ["label_classifier_1", "label_classifier_2", "label_classifier_3"]

        self.label_output = ["label_output_1", "label_output_2", "label_output_3"]

        self.text = ["Configuration 1:\n- TfidfVectorizer\n- MultinomialNB",
                     "Configuration 2:\n- TfidfVectorizer\n- LogisticRegression",
                     "Configuration 3:\n- TfidfVectorizer\n- SGDClassifier"]

        for index in range(len(self.label)):
            self.label[index] = customtkinter.CTkLabel(master=self.frame_home,
                                                       text=self.text[index],
                                                       width=10,
                                                       height=10,
                                                       justify=tkinter.LEFT)
            self.label[index].grid(row=index + 1, column=0, pady=15, padx=15, sticky="nwe")
            self.label_output[index] = customtkinter.CTkLabel(master=self.frame_home,
                                                              text="",
                                                              height=70,
                                                              corner_radius=6,
                                                              fg_color=("white", "gray38"),
                                                              justify=tkinter.LEFT)
            self.label_output[index].grid(row=index + 1, column=1, pady=15, padx=15, sticky="nwe")

        # ============ frame_right ============
        self.button_classify = customtkinter.CTkButton(master=self.frame_button_classify,
                                                       text="Classify",
                                                       border_width=2,
                                                       fg_color=None,
                                                       command=self.button_event_classify)
        self.button_classify.grid(row=8, column=1, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.menu_appearance.set("System")

        self.windowConf = None
        self.windowStats = None

    def button_event_classify(self):
        """
        Method to display class prediction and probability of classifiers
        """
        self.label_output[0].configure(
            text=self.classifierTfidfMultinomialNB.calculate_class(self.text_input.get("0.0", "end")))
        self.label_output[1].configure(
            text=self.classifierTfidfLogReg.calculate_class(self.text_input.get("0.0", "end")))
        self.label_output[2].configure(
            text=self.classifierTfidfSGD.calculate_class(self.text_input.get("0.0", "end")))

    def reload_config_classifier(self):
        """
        Method to initialize classifiers
        """
        self.classifierTfidfMultinomialNB.reload_config()
        self.classifierTfidfLogReg.reload_config()
        self.classifierTfidfSGD.reload_config()

    def button_event_config(self):
        """
        Method to open configuration window
        """
        self.windowConf = WindowConfiguration(self)
        self.windowConf.mainloop()

    def button_event_statistics(self):
        """
        Method to open statistics window
        """
        self.windowStats = WindowStatistics(self)
        self.windowStats.mainloop()

    def button_event_test(self):
        """
        Method to open statistics window
        """
        self.windowStats = WindowTest(self)
        self.windowStats.mainloop()

    @staticmethod
    def change_appearance_mode(new_appearance_mode):
        """
        Method to open appearance of the application
        """
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self):
        """
        Method to close all windows of application
        """
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.windowConf.on_closing()
            except:
                pass
            try:
                self.windowStats.on_closing()
            except:
                pass
            self.destroy()
