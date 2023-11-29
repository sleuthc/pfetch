import os.path
import sys
import requests

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QCheckBox, QPushButton,
                               QScrollArea, QGroupBox, QApplication, QMessageBox, QInputDialog, QFileDialog,
                               QTreeWidgetItem)

from PySide6.QtCore import QFile, QTextStream, Signal, QRunnable, QThreadPool, QObject, QSemaphore, Qt
from PySide6.QtGui import QIcon
from configparser import ConfigParser

from src.backend.shared_functions import (strip_title, check_video, check_if_video_exists, setup_config_file,
                                          logger_error, logger_debug, correct_output_path)

from src.frontend.ui_form import Ui_Porn_Fetch_Widget
from src.frontend.License import Ui_License
from src.frontend import ressources_rc  # This is needed for the Stylesheet and Icons
from phub import Quality, Client, locals, errors, download
from hqporner_api.api import API

categories = [attr for attr in dir(locals.Category) if
              not callable(getattr(locals.Category, attr)) and not attr.startswith("__")]

total_file_size = 0
downloaded_size = 0



def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    qmsg_box = QMessageBox()
    qmsg_box.setText(text)
    qmsg_box.exec()


def show_get_text_dialog(self, title, text):
    name, ok = QInputDialog.getText(self, f'{title}', f'{text}:')
    if ok:
        return name


class WorkerSignals(QObject):
    progress = Signal(int)
    completed = Signal()


class DownloadProgressSignal(QObject):
    """Sends the current download progress to the main UI to update the progressbar."""
    progress = Signal(int, int)
    total_progress = Signal(int, int)


class QTreeWidgetSignal(QObject):
    progress = Signal(str)
    get_total = Signal(str, Quality)
    start_undefined_range = Signal()
    stop_undefined_range = Signal(int)


class DownloadThread(QRunnable):
    signal = Signal()

    def __init__(self, video, quality, output_path, threading_mode):
        super(DownloadThread, self).__init__()

        self.video = video
        self.quality = quality
        self.output_path = output_path
        self.threading_mode = threading_mode
        self.downloader = None
        self.signals = DownloadProgressSignal()
        self.signals_completed = WorkerSignals()

    def callback(self, pos, total, website="pornhub"):

        global downloaded_size, total_file_size

        if website == "pornhub":
            print("PornHub")
            downloaded_size += 1  # or some calculation based on segments
        elif website == "hqporner":
            downloaded_size = pos  # For the second website, use the current downloaded size

        self.signals.progress.emit(downloaded_size, total_file_size)
        self.signals.total_progress.emit(downloaded_size, total_file_size)

    def run(self):
        try:
            if self.threading_mode == 2:
                self.downloader = download.threaded(max_workers=20, timeout=15)

            elif self.threading_mode == 1:
                self.downloader = download.FFMPEG

            elif self.threading_mode == 0:
                self.downloader = download.default

            if str(self.video).endswith(".html"):
                API().download(url=self.video, quality="highest", output_path=self.output_path, callback=self.callback,
                               no_title=True)

            else:
                self.video.download(downloader=self.downloader, path=self.output_path, quality=self.quality,
                                    display=self.callback)

        finally:
            self.signals_completed.completed.emit()


class QTreeWidgetDownloadThread(QRunnable):

    def __init__(self, treeWidget, semaphore, quality):
        super(QTreeWidgetDownloadThread, self).__init__()
        self.treeWidget = treeWidget
        self.semaphore = semaphore
        self.signals = QTreeWidgetSignal()
        self.quality = quality

    def run(self):
        video_urls = []
        video_urls_pornhub = []
        video_urls_hqporner = []
        video_objects_pornhub = []

        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == Qt.Checked:
                video_urls.append(item.data(0, Qt.UserRole))

        self.signals.start_undefined_range.emit()

        global total_file_size, downloaded_size
        for url in video_urls:
            if str(url).endswith(".html"):
                video_urls_hqporner.append(url)

            else:
                video_objects_pornhub.append(check_video(url, language="en"))  # Not used for downloading, so language doesn't matter

        total_file_size = sum(
            [len(list(video.get_segments(quality=self.quality))) for video in video_objects_pornhub]
        )
        total_file_size += sum(
            [API().get_total_size(url, "highest") for url in video_urls_hqporner]
        )

        self.signals.stop_undefined_range.emit(total_file_size)

        for video_url in video_urls_pornhub:
            logger_debug(f"Downloading: {video_url}")
            self.semaphore.acquire()
            logger_debug("Semaphore Acquired")
            self.signals.progress.emit(video_url)

        for video_url in video_urls_hqporner:
            logger_debug(f"Downloading: {video_url}")
            self.semaphore.acquire()
            self.signals.progress.emit(video_url)


class License(QWidget):
    """ License class to display the GPL 3 License to the user."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_widget = None
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        self.ui = Ui_License()
        self.ui.setupUi(self)
        self.ui.button_accept.clicked.connect(self.accept)
        self.ui.button_deny.clicked.connect(self.denied)

    def check_license_and_proceed(self):
        if self.conf["License"]["accepted"] == "true":
            self.show_main_window()

        else:
            self.show()  # Show the license widget

    def accept(self):
        self.conf.set("License", "accepted", "true")
        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
            config_file.close()

        self.show_main_window()

    def denied(self):
        self.conf.set("License", "accepted", "false")
        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
            config_file.close()
            self.close()
            sys.exit(0)

    def show_main_window(self):
        """ If license was accepted, the License widget is closed and the main widget will be shown."""
        self.close()
        self.main_widget = PornFetch()
        self.main_widget.show()


class CategoryFilterWindow(QWidget):
    data_selected = Signal((str, list))

    def __init__(self, categories):
        super().__init__()
        self.excluded_categories = None
        self.selected_category = None
        self.radio_buttons = {}
        self.checkboxes = {}
        self.categories = categories

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        left_layout = QVBoxLayout()
        left_group = QGroupBox("Select Category")

        for category in self.categories:
            radio_button = QRadioButton(category)
            left_layout.addWidget(radio_button)
            self.radio_buttons[category] = radio_button

        left_group.setLayout(left_layout)

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setWidget(left_group)

        right_layout = QVBoxLayout()
        right_group = QGroupBox("Exclude Categories")

        for category in self.categories:
            checkbox = QCheckBox(category)
            right_layout.addWidget(checkbox)
            self.checkboxes[category] = checkbox

        right_group.setLayout(right_layout)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setWidget(right_group)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.on_apply)

        hlayout = QHBoxLayout()
        hlayout.addWidget(left_scroll)
        hlayout.addWidget(right_scroll)

        layout.addLayout(hlayout)
        layout.addWidget(apply_button)
        self.setLayout(layout)

    def on_apply(self):
        selected_category = None
        excluded_categories = []

        for category, radio_button in self.radio_buttons.items():
            if radio_button.isChecked():
                selected_category = category

        for category, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                excluded_categories.append(category)

        self.selected_category = selected_category
        self.excluded_categories = excluded_categories
        self.data_selected.emit(self.selected_category, self.excluded_categories)
        self.close()


class PornFetch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Variable initialization:

        self.semaphore = None
        self.native_languages = None
        self.directory_system_map = None
        self.threading_mode_map = None
        self.threading_map = None
        self.language_map = None
        self.quality_map = None
        self.selected_category = None
        self.excluded_categories_filter = None
        self.client = None
        self.api_language = None
        self.search_limit = None
        self.semaphore_limit = None
        self.quality = None
        self.output_path = None
        self.threading_mode = None
        self.threading = None
        self.directory_system = None

        self.threadpool = QThreadPool()

        # Configuration file:
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        # UI relevant initialization:
        self.ui = Ui_Porn_Fetch_Widget()
        self.ui.setupUi(self)
        self.button_connectors()
        self.load_icons()
        self.settings_maps_initialization()
        self.load_user_settings()
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.update_settings()

    def load_icons(self):
        """a simple function to load the icons for the buttons"""
        self.ui.button_switch_search.setIcon(QIcon(":/images/graphics/search.svg"))
        self.ui.button_switch_home.setIcon(QIcon(":/images/graphics/download.svg"))
        self.ui.button_switch_settings.setIcon(QIcon(":/images/graphics/settings.svg"))
        self.ui.button_switch_credits.setIcon(QIcon(":/images/graphics/information.svg"))
        self.setWindowIcon(QIcon(":/images/graphics/logo_transparent.ico"))
        logger_debug("Loaded Icons!")

    def button_connectors(self):
        """a function to link the buttons to their functions"""

        # Menu Bar Switch Button Connections
        self.ui.button_switch_home.clicked.connect(self.switch_to_home)
        self.ui.button_switch_search.clicked.connect(self.switch_to_search)
        self.ui.button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.button_output_path_select.clicked.connect(self.select_output_path)

        # Video Download Button Connections
        self.ui.button_download.clicked.connect(self.start_single_video)
        self.ui.button_model.clicked.connect(self.start_model)
        self.ui.button_tree_download.clicked.connect(self.download_tree_widget)
        self.ui.button_tree_select_all.clicked.connect(self.select_all_items)
        self.ui.button_tree_unselect_all.clicked.connect(self.unselect_all_items)
        self.ui.button_open_file.clicked.connect(self.select_url_file)

        # Account Button Connections
        self.ui.button_login.clicked.connect(self.login)
        self.ui.button_get_recommended_videos.clicked.connect(self.get_recommended_videos)
        self.ui.button_get_watched_videos.clicked.connect(self.get_watched_videos)
        self.ui.button_get_liked_videos.clicked.connect(self.get_liked_videos)

        # Help Button Connections
        self.ui.button_semaphore_help.clicked.connect(self.button_semaphore_help)
        self.ui.button_threading_mode_help.clicked.connect(self.button_threading_mode_help)
        self.ui.button_directory_system_help.clicked.connect(self.button_directory_system_help)

        # Settings
        self.ui.button_settings_apply.clicked.connect(self.save_user_settings)

        logger_debug("Connected Buttons!")

    def switch_to_home(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(0)

    def switch_to_search(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(1)

    def switch_to_settings(self):
        self.ui.stacked_widget_main.setCurrentIndex(1)

    def switch_to_credits(self):
        self.ui.stacked_widget_main.setCurrentIndex(2)

    """
    The following are functions used by different other functions to handle data over different classes / threads.
    Mostly by using signals and slot connectors. I don't recommend anyone to change stuff here!
    (It's already complicated enough, even with the Documentation)
    """

    def handle_selected_data(self, selected_category, excluded_categories):
        """
        Receives the selected and excluded categories from the Category class. Needed for video searching.
        """
        self.selected_category = selected_category
        self.excluded_categories_filter = excluded_categories

    def update_total_progressbar(self, value, maximum):
        self.ui.progressbar_total.setMaximum(maximum)
        self.ui.progressbar_total.setValue(value)

    def update_progressbar(self, value, maximum):
        self.ui.progressbar_current.setMaximum(maximum)
        self.ui.progressbar_current.setValue(value)

    def download_completed(self):
        logger_debug("Download Completed!")
        self.semaphore.release()

    def start_undefined_progress(self):
        self.ui.progressbar_total.setRange(0, 0)

    def stop_undefined_progress(self, maximum):
        self.ui.progressbar_total.setRange(0, maximum)

    """
    The following functions are needed for the settings. They apply, load, and save user settings.
    """

    def get_quality(self):
        """Returns the quality selected by the user"""
        if self.ui.radio_quality_best.isChecked():
            self.quality = Quality.BEST

        elif self.ui.radio_quality_half.isChecked():
            self.quality = Quality.HALF

        elif self.ui.radio_quality_worst.isChecked():
            self.quality = Quality.WORST

    def get_api_language(self):
        """Returns the API Language. Will be used by the API to return correct video titles etc..."""

        if self.ui.radio_api_language_custom.isChecked():
            if self.api_language in self.native_languages:
                language = show_get_text_dialog(title="API Language", text="""
                Please enter the language code for your language.  Example: en, de, fr, ru --=>:""", self=self)
                self.api_language = language

        elif self.ui.radio_api_language_chinese.isChecked():
            self.api_language = "zh"

        elif self.ui.radio_api_language_english.isChecked():
            self.api_language = "en"

        elif self.ui.radio_api_language_french.isChecked():
            self.api_language = "fr"

        elif self.ui.radio_api_language_german.isChecked():
            self.api_language = "de"

        elif self.ui.radio_api_language_russian.isChecked():
            self.api_language = "ru"

    def get_output_path(self):
        """Returns the output path for the videos selected by the user"""
        output_path = self.ui.lineedit_output_path.text()
        logger_debug(f"Output Path: {output_path}")
        if not os.path.exists(output_path):
            ui_popup("The specified output path doesn't exist. If you think, this is an error, please report it!")

        else:
            self.output_path = output_path

    def get_semaphore_limit(self):
        """Returns the semaphore limit selected by the user"""
        value = self.ui.spinbox_semaphore.value()
        if value >= 1:
            self.semaphore_limit = value

    def get_threading_mode(self):
        """Returns the threading mode selected by the user"""
        if self.ui.radio_threading_mode_default.isChecked():
            self.threading_mode = 0

        elif self.ui.radio_threading_mode_ffmpeg.isChecked():
            self.threading_mode = 1

        elif self.ui.radio_threading_mode_high_performance.isChecked():
            self.threading_mode = 2

    def get_threading(self):
        """Checks if threading should be used or not"""
        if self.ui.radio_threading_yes.isChecked():
            self.threading = True

        elif self.ui.radio_threading_no.isChecked():
            self.threading = False

    def get_search_limit(self):
        """Returns the search limit selected by the user"""
        search_limit = self.ui.spinbox_searching.value() if self.ui.spinbox_searching.value() >= 1 else 50
        self.search_limit = search_limit

    def is_directory_system(self):
        """Checks if the directory system was enabled"""
        if self.ui.radio_directory_system_yes.isChecked():
            self.directory_system = True

        elif self.ui.radio_directory_system_no.isChecked():
            self.directory_system = False

    def update_settings(self):
        """Updates all settings, so that the cache gets reloaded."""
        self.get_threading()
        self.get_search_limit()
        self.get_threading_mode()
        self.get_quality()
        self.get_api_language()
        self.get_output_path()
        self.is_directory_system()
        self.get_semaphore_limit()

    def settings_maps_initialization(self):
        self.native_languages = ["en", "de", "fr", "ru", "zh"]

        # Maps for settings and corresponding UI elements
        self.quality_map = {
            "best": self.ui.radio_quality_best,
            "half": self.ui.radio_quality_half,
            "worst": self.ui.radio_quality_worst
        }

        self.language_map = {
            "en": self.ui.radio_api_language_english,
            "ru": self.ui.radio_api_language_russian,
            "fr": self.ui.radio_api_language_french,
            "de": self.ui.radio_api_language_german,
            "zh": self.ui.radio_api_language_chinese
        }

        self.threading_map = {
            "yes": self.ui.radio_threading_yes,
            "no": self.ui.radio_threading_no
        }

        self.threading_mode_map = {
            "2": self.ui.radio_threading_mode_high_performance,
            "1": self.ui.radio_threading_mode_ffmpeg,
            "0": self.ui.radio_threading_mode_default
        }

        self.directory_system_map = {
            "1": self.ui.radio_directory_system_yes,
            "0": self.ui.radio_directory_system_no
        }

    def load_user_settings(self):
        """Loads the user settings from the configuration file and applies them."""

        # Apply settings
        self.quality_map.get(self.conf.get("Video", "quality")).setChecked(True)
        self.language_map.get(self.conf.get("Video", "language")).setChecked(True)
        self.threading_map.get(self.conf.get("Performance", "threading")).setChecked(True)
        self.threading_mode_map.get(self.conf.get("Performance", "threading_mode")).setChecked(True)
        self.directory_system_map.get(self.conf.get("Video", "directory_system")).setChecked(True)

        self.ui.spinbox_semaphore.setValue(int(self.conf.get("Performance", "semaphore")))
        self.ui.spinbox_searching.setValue(int(self.conf.get("Video", "search_limit")))
        self.ui.lineedit_output_path.setText(self.conf.get("Video", "output_path"))

        self.semaphore_limit = self.conf.get("Performance", "semaphore")
        self.search_limit = self.conf.get("Video", "search_limit")
        self.output_path = self.conf.get("Video", "output_path")
        self.api_language = self.conf.get("Video", "language")

        if not self.api_language in self.native_languages:
            self.ui.radio_api_language_custom.setChecked(True)

        self.semaphore = QSemaphore(int(self.semaphore_limit))
        logger_debug("Loaded User Settings!")

    def save_user_settings(self):
        """Saves the user settings to the configuration file based on the UI state."""

        # Save quality setting
        for quality, radio_button in self.quality_map.items():
            if radio_button.isChecked():
                self.conf.set("Video", "quality", quality)

        # Save language setting
        for language, radio_button in self.language_map.items():
            if radio_button.isChecked():
                self.conf.set("Video", "language", language)

        # Save threading setting
        for threading, radio_button in self.threading_map.items():
            if radio_button.isChecked():
                self.conf.set("Performance", "threading", threading)

        # Save threading mode
        for mode, radio_button in self.threading_mode_map.items():
            if radio_button.isChecked():
                self.conf.set("Performance", "threading_mode", mode)

        # Save directory system setting
        for system, radio_button in self.directory_system_map.items():
            if radio_button.isChecked():
                self.conf.set("Video", "directory_system", system)

        # Save other settings
        self.conf.set("Performance", "semaphore", str(self.ui.spinbox_semaphore.value()))
        self.conf.set("Video", "search_limit", str(self.ui.spinbox_searching.value()))
        self.conf.set("Video", "output_path", self.ui.lineedit_output_path.text())
        self.conf.set("Video", "language", self.api_language)

        self.update_settings()

        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)

        logger_debug("Saved User Settings!")

    """
    The following are functions used by the treeWidget.
    """

    def add_to_tree_widget(self, iterator, search_limit):
        self.ui.treeWidget.clear()

        try:
            logger_debug(f"Search Limit: {str(search_limit)}")
            for i, video in enumerate(iterator[0:int(search_limit)], start=1):
                item = QTreeWidgetItem(self.ui.treeWidget)

                if str(video).endswith(".html"):
                    item.setText(0, f"{i}) {API().extract_title(video)}")
                    item.setData(0, Qt.UserRole, video)

                else:
                    item.setText(0, f"{i}) {video.title}")
                    item.setData(0, Qt.UserRole, video.url)

                item.setCheckState(0, Qt.Unchecked)  # Adds a checkbox

        except errors.NoResult:
            pass

    def download_tree_widget(self):
        semaphore = self.semaphore
        treeWidget = self.ui.treeWidget
        quality = self.quality
        download_tree_thread = QTreeWidgetDownloadThread(treeWidget=treeWidget, semaphore=semaphore, quality=quality)
        download_tree_thread.signals.progress.connect(self.tree_widget_completed)
        download_tree_thread.signals.start_undefined_range.connect(self.start_undefined_progress)
        download_tree_thread.signals.stop_undefined_range.connect(self.stop_undefined_progress)
        self.threadpool.start(download_tree_thread)

    def tree_widget_completed(self, url):
        self.load_video(url, semaphore_acquire=False)

    def unselect_all_items(self):
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.Unchecked)

    def select_all_items(self):
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.Checked)

    """
    The following functions are used by the QFileDialog in order to let the user select directories / files.
    """

    def select_output_path(self):
        """User can select the directory from a pop-up (QFileDialog) list"""
        directory = QFileDialog.getExistingDirectory()
        if os.path.exists(directory):  # Should always be the case hopefully
            self.ui.lineedit_output_path.setText(directory)
            self.output_path = directory

    def select_url_file(self):
        file = QFileDialog.getOpenFileUrl(self, "Select the URL file")
        file_path = file[0].toLocalFile()
        self.ui.lineedit_file.setText(file_path)
        logger_debug(f"Processing file: {file_path}")
        self.process_url_file()
    """
    The following functions are used by the help buttons in order to show help messages.
    """

    def button_semaphore_help(self):
        text = f"""
The Semaphore is a tool to limit the number of simultaneous actions / downloads.

For example: If the semaphore is set to 1, only 1 video will be downloaded at the same time.
If the semaphore is set to 4, 4 videos will be downloaded at the same time. Changing this is only useful, if
you have a really good internet connection and a good system.
"""
        ui_popup(text)

    def button_threading_mode_help(self):
        text = """
The different threading modes are used for different scenarios. 

1) High Performance:  Uses a class of workers to download multiple video segments at a time. Can be really fast if you
have a very strong internet connection. Maybe not great for low end systems.

2) FFMPEG:  ffmpeg is a tool for converting media files. ffmpeg will download every video segment and merge it directly
into the video file. This removes an extra step from the default method and is therefore a lot faster, but still not as 
good as high performance.

3) Default:  The default download mode will just download one video segment after the next one. If you get a lot of 
timeouts this can really slow down the process, as we need to wait for PornHub to return the video segments.
With the High Performance method, we can just download other segments while waiting which makes it so fast.
"""
        ui_popup(text)

    def button_directory_system_help(self):
        text = """
The directory system will save videos in an intelligent way. If you download 3 videos form one Pornstar and 5 videos 
from another, Porn Fetch will automatically make folders for it and move the 3 videos into that one folder and the other
5 into the other. (This will still apply with your selected output path)

This can be helpful for organizing stuff, but is a more advanced feature, so the majority of users won't use it probably.
"""

        ui_popup(text)

    """
    The following functions are used for the Account
    """

    def login(self):

        username = self.ui.lineedit_username.text()
        password = self.ui.lineedit_password.text()

        try:
            self.get_api_language()
            self.client = Client(username=username, password=password, language=self.api_language)
            logger_debug("Login Successful!")

        except errors.LoginFailed:
            logger_error("Login Failed!")
            ui_popup("Login Failed, please check your credentials and try again!")

    def get_watched_videos(self):
        if not self.client.logged:
            self.add_to_tree_widget(self.client.account.watched, search_limit=500)

    def get_liked_videos(self):
        if not self.client.logged:
            self.add_to_tree_widget(self.client.account.liked, search_limit=500)

    def get_recommended_videos(self):
        if not self.client.logged:
            self.add_to_tree_widget(self.client.account.recommended, search_limit=500)

    """
    The following functions are used to start special processes.
    Downloading and Searching. So this is actually the core or most important stuff,
    But I have my focus at the smaller functions to work as 'backend' so that I don't need to code so much
    and the whole process is more efficient with it.
    """

    def start_single_video(self):
        url = self.ui.lineedit_url.text()
        self.load_video(url)

    def start_model(self):
        model = self.ui.lineedit_model_url.text()
        api_language = self.api_language
        search_limit = self.search_limit
        client = Client(language=api_language)
        model_object = client.get_user(model)
        videos = model_object.videos
        self.add_to_tree_widget(videos, search_limit=search_limit)

    def process_url_file(self):
        self.get_api_language()
        api_language = self.api_language
        file = self.ui.lineedit_file.text()
        hqporner_urls = []
        pornhub_objects = []

        with open(file, "r") as url_file:
            content = url_file.read().splitlines()

        for url in content:
            if url.endswith(".html"):
                hqporner_urls.append(url)

            else:
                pornhub_objects.append(check_video(url, language=api_language))

        iterator = hqporner_urls + pornhub_objects
        self.add_to_tree_widget(iterator, search_limit=len(iterator))

    def load_video(self, url, semaphore_acquire=True):
        if semaphore_acquire:
            logger_debug("Acquiring Semaphore")
            self.semaphore.acquire()

        self.update_settings()
        output_path = self.output_path
        api_language = self.api_language
        threading_mode = self.threading_mode
        directory_system = self.directory_system
        quality = self.quality

        if url.endswith(".html"):
            title = API().extract_title(url)
            video = url

        else:
            video = check_video(url, api_language)
            title = video.title

        output_path = correct_output_path(output_path)
        stripped_title = strip_title(title)
        logger_debug(f"Loading Video: {stripped_title}")

        if directory_system:
            if url.endswith(".html"):
                author = API().extract_actress(url)[0]

            else:
                author = video.author.name

            if not os.path.exists(f"{output_path}{author}"):
                os.mkdir(output_path + author)

            print(f"old out: {output_path}")
            print(f"Author: {author}")
            print(f"Sep: {os.sep}")
            print(f"Stripped_title: {stripped_title}")
            output_path = f"{output_path}{author}{os.sep}{stripped_title}.mp4"
            print(output_path)
            output_path.strip("'")

        else:
            output_path = f"{output_path}{stripped_title}.mp4"
            output_path.strip("'")

        if not check_if_video_exists(video, output_path):
            if self.threading:
                print(logger_debug(f"OUT: {output_path}"))
                logger_debug("Processing Thread")
                self.process_video_thread(output_path=output_path, video=video, threading_mode=threading_mode,
                                          quality=quality)

            elif not self.threading:
                self.process_video_without_thread(output_path, video, quality)

        else:
            self.semaphore.release()
            global downloaded_segments
            downloaded_segments += len(list(video.get_segments(quality=quality)))


    def process_video_thread(self, output_path, video, threading_mode, quality):
        """Checks which of the three types of threading the user selected and handles them."""
        self.download_thread = DownloadThread(video=video, output_path=output_path, quality=quality,
                                              threading_mode=threading_mode)
        self.download_thread.signals.progress.connect(self.update_progressbar)
        self.download_thread.signals.total_progress.connect(self.update_total_progressbar)
        self.download_thread.signals_completed.completed.connect(self.download_completed)
        self.threadpool.start(self.download_thread)
        logger_debug("Started Download Thread!")

    def process_video_without_thread(self, output_path, video, quality):
        """Downloads the video without any threading.  (NOT RECOMMENDED!)"""
        logger_debug("Downloading without threading! Note, the GUI will freeze until the video is downloaded!!!")
        video.download(path=output_path, quality=quality, downloader=download.default)
        logger_debug("Download Completed!")

    def search_videos(self):
        """I don't know how this function even works. Ask ChatGPT about it. No joke, I don't understand it."""
        include_filters = []
        exclude_filters = []

        filter_objects = {
            'include': [self.selected_category],
            'exclude': [self.excluded_categories_filter]
        }

        for action, filters in filter_objects.items():
            for filter_object in filters:
                if isinstance(filter_object, locals.Param):
                    if action == 'include':
                        include_filters.append(filter_object)
                    elif action == 'exclude':
                        exclude_filters.append(filter_object)
                else:
                    print(f"Invalid filter")

        if include_filters:
            combined_include_filter = include_filters[0]
            for filter_object in include_filters[1:]:
                combined_include_filter |= filter_object
        else:
            combined_include_filter = None

        if exclude_filters:
            combined_exclude_filter = exclude_filters[0]
            for filter_object in exclude_filters[1:]:
                combined_exclude_filter -= filter_object
        else:
            combined_exclude_filter = None

        query = self.ui.lineedit_search_query.text()

        if combined_include_filter and combined_exclude_filter:
            final_filter = combined_include_filter - combined_exclude_filter
            query_object = self.client.search(query, final_filter)
        elif combined_include_filter:
            query_object = self.client.search(query, combined_include_filter)
        elif combined_exclude_filter:
            query_object = self.client.search(query, -combined_exclude_filter)
        else:
            query_object = self.client.search(query)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        """
        I had many problems with coding in general where something didn't work but the translations are the hardest
        thing I've ever done. Now where I've understand it it makes sense but the Qt documentation is a piece of shit...
        """

        """# Obtain the system's locale
        locale = QLocale.system()
        # Get the language code (e.g., "de" for German)
        language_code = locale.name().split('_')[0]
        # Construct the path to the translation file
        path = f":/translations/translations/{language_code}.qm"

        translator = QTranslator(app)
        if translator.load(path):
            logging(f"{language_code} translation loaded")
            app.installTranslator(translator)
        else:
            logging(f"Failed to load {language_code} translation")
        """
        file = QFile(":/style/stylesheet.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

        widget = License()  # Starts License widget and checks if license was accepted.
        widget.check_license_and_proceed()

    except PermissionError:
        ui_popup("Insufficient Permissions to access something. Please run Porn Fetch as root / admin")

    except ConnectionResetError:
        ui_popup("Connection was reset. Are you connected to a public wifi or a university's wifi? ")
    except ConnectionError:
        ui_popup("Connection Error, please make sure you have a stable internet connection")

    except KeyboardInterrupt:
        sys.exit(0)

    except requests.exceptions.SSLError:
        ui_popup("SSLError: Your connection is blocked by your ISP / IT administrator (Firewall). If you are in a "
                 "University or at school, please connect to a VPN / Proxy")

    except TypeError:
        pass

    except OSError as e:
        ui_popup(f"This error shouldn't happen. If you still see it it's REALLY important that you report the "
                 f"following: {e}")

    except ZeroDivisionError:
        pass

    sys.exit(app.exec())


if __name__ == "__main__":
    setup_config_file()
    main()
