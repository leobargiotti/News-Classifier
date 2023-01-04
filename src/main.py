from gui.WindowHome import WindowHome
import os
from utils.utils import download_if_non_existent

if __name__ == '__main__':
    """
    Main to open GUI application of News Classifier
    Reads preferences from file 'config.ini'
    """

    download_if_non_existent('corpora/stopwords', 'stopwords')
    download_if_non_existent('tokenizers/punkt', 'punkt')

    # directory main.py
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    app = WindowHome()
    app.mainloop()
