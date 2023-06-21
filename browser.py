from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

translations = {
    "en": {
        "window_title": "Schächner Web Browser",
        "go_btn": "Go",
        "back_btn": "<",
        "forward_btn": ">",
        "new_tab_btn": "+",
        "bookmark_btn": "Bookmark",
        "settings_btn": "Settings",
        "bookmark_added_title": "Bookmark Added",
        "bookmark_added_msg": "Bookmark has been added.",
        "settings_title": "Settings",
        "language_label": "Select Language:",
        "save_btn": "Save",
        "history_btn": "History",
        "open_bookmarks": "Open Bookmarks",
        "open_history": "Open History",
        "open_settings": "Open Settings"
    },
    "de": {
        "window_title": "Schächner Webbrowser",
        "go_btn": "Suche",
        "back_btn": "<",
        "forward_btn": ">",
        "new_tab_btn": "+",
        "bookmark_btn": "Lesezeichen",
        "settings_btn": "Einstellungen",
        "bookmark_added_title": "Lesezeichen hinzugefügt",
        "bookmark_added_msg": "Lesezeichen wurde hinzugefügt.",
        "settings_title": "Einstellungen",
        "language_label": "Sprache auswählen:",
        "save_btn": "Speichern",
        "history_btn": "Verlauf",
        "open_bookmarks": "Lesezeichen öffnen",
        "open_history": "Verlauf öffnen",
        "open_settings": "Einstellungen öffnen"
    }
}

class TabWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setStyleSheet(
        """
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                padding: 8px 12px;
                margin: 0px;
                background-color: #f2f2f2;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border-bottom: 2px solid #f2f2f2;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 2px solid #2980b9;
            }
            QTabBar::tab:hover {
                background-color: #e3e3e3;
            }
            QTabBar::tab:selected:hover {
                background-color: #ffffff;
            }
            QTabBar::close-button {
                image: url(close_icon.png);
                subcontrol-position: right;
                subcontrol-origin: padding;
                margin-left: 0px;
            }
            QTabBar::close-button:hover {
                image: url(close_icon_hover.png);
            }
            """
        )

    def add_tab(self, url):
        browser = CustomWebView()
        browser.setUrl(QUrl(url))
        browser.page().titleChanged.connect(lambda title: self.set_tab_title(browser, title))
        self.addTab(browser, "")
    
        tab_index = self.indexOf(browser)
        self.set_tab_title(browser, browser.page().title())
        self.setCurrentIndex(tab_index)

    def close_tab(self, index):
        widget = self.widget(index)
        widget.deleteLater()
        self.removeTab(index)

    def set_tab_title(self, browser, title):
        index = self.indexOf(browser)
        if index != -1:
            displayed_title = title[:10] + "..." if len(title) > 10 else title
            self.setTabText(index, displayed_title)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search_engine = "Google"  # Standard-Suchmaschine festlegen

        self.setWindowTitle(translations["en"]["window_title"])
        
        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        self.tab_widget = TabWidget(self)

        self.url_bar = QLineEdit()
        self.url_bar.setMaximumHeight(10)
        self.url_bar.returnPressed.connect(self.navigate)

        self.go_btn = QPushButton(translations["en"]["go_btn"])
        self.go_btn.setMinimumHeight(30)

        self.history_btn = QPushButton(translations["en"]["history_btn"])
        self.history_btn.setMinimumHeight(30)

        self.new_tab_btn = QPushButton(translations["en"]["new_tab_btn"])
        self.new_tab_btn.setMinimumHeight(30)
        self.new_tab_btn.setFixedSize(500, 30)

        self.back_btn = QPushButton(translations["en"]["back_btn"])
        self.back_btn.setMinimumHeight(30)
        self.back_btn.setFixedSize(20, 30)

        self.forward_btn = QPushButton(translations["en"]["forward_btn"])
        self.forward_btn.setMinimumHeight(30)
        self.forward_btn.setFixedSize(0, 30)

        self.bookmark_btn = QPushButton(translations["en"]["bookmark_btn"])
        self.bookmark_btn.setMinimumHeight(30)

        self.settings_btn = QPushButton(translations["en"]["settings_btn"])
        self.settings_btn.setMinimumHeight(30)

        self.go_btn.clicked.connect(self.navigate)
        self.back_btn.clicked.connect(self.go_back)
        self.forward_btn.clicked.connect(self.go_forward)
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        self.bookmark_btn.clicked.connect(self.add_bookmark)
        self.history_btn.clicked.connect(self.show_history)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.tab_widget)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.add_new_tab()

        self.bookmarks = []

        self.language = "en"

        self.history = []

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)  # Nur Icons anzeigen
        self.toolbar.setIconSize(QSize(20, 20))

        self.history_btn = QAction(QIcon("history_icon.png"), "History", self)
        self.history_btn.triggered.connect(self.show_history)
        self.toolbar.addAction(self.history_btn)

        self.bookmarks_btn = QAction(QIcon("bookmarks_icon.png"), "Bookmarks", self)
        self.bookmarks_btn.triggered.connect(self.show_bookmarks)
        self.toolbar.addAction(self.bookmarks_btn)

        self.settings_btn = QAction(QIcon("settings_icon.png"), "Settings", self)
        self.settings_btn.triggered.connect(self.open_settings)
        self.toolbar.addAction(self.settings_btn)

        self.search_toolbar = self.addToolBar("Search Menu")
        self.search_toolbar.setStyleSheet("QToolButton { text-align: left; }")

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        self.search_toolbar.addWidget(self.url_bar)

        self.go_btn = QPushButton(QIcon("go_icon.png"), translations["en"]["go_btn"])
        self.go_btn.clicked.connect(self.navigate)
        self.search_toolbar.addWidget(self.go_btn)

        self.new_tab_btn = QPushButton(QIcon("go_icon.png"), translations["en"]["new_tab_btn"])
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        self.search_toolbar.addWidget(self.new_tab_btn)

        self.back_btn = QPushButton(QIcon("go_icon.png"), translations["en"]["back_btn"])
        self.back_btn.clicked.connect(self.go_back)
        self.search_toolbar.addWidget(self.back_btn)

        self.forward_btn = QPushButton(QIcon("go_icon.png"), translations["en"]["forward_btn"])
        self.forward_btn.clicked.connect(self.go_forward)
        self.search_toolbar.addWidget(self.forward_btn)

        self.bookmark_btn = QPushButton(QIcon("go_icon.png"), translations["en"]["bookmark_btn"])
        self.bookmark_btn.clicked.connect(self.add_bookmark)
        self.search_toolbar.addWidget(self.bookmark_btn)

        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.cookieStore().cookieAdded.connect(self.cookie_added)
    def cookie_added(self, cookie):
        print("Cookie added:", cookie.toRawForm())

        

    def translate(self, key):
        return translations[self.language].get(key, key)

    def navigate(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            url = self.url_bar.text()
            if "." not in url:
                url = "https://www.google.com/search?q=" + url.replace(" ", "+")
            elif not url.startswith("https://") and not url.startswith("http://"):
                url = "https://" + url
            self.load_url(current_tab, url)
            self.history.append(url)


    def load_url(self, tab, url):
        tab.setUrl(QUrl(url))

    def go_back(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.back()
        if len(self.history) > 1:
            url = self.history[-2]
            self.load_url(current_tab, url)
            self.history.pop()

    def go_forward(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.forward()

    def add_new_tab(self):
        self.tab_widget.add_tab("https://www.google.com")

    def add_bookmark(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            url = current_tab.url().toString()
            title = current_tab.page().title()
            bookmark = {"url": url, "title": title}
            self.bookmarks.append(bookmark)
            QMessageBox.information(self, translations[self.language]["bookmark_added_title"], translations[self.language]["bookmark_added_msg"])

    def show_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle(translations[self.language]["history_btn"])
        history_dialog.setModal(True)

        layout = QVBoxLayout()

        history_list = QListWidget()
        for url in self.history:
            item = QListWidgetItem(url)
            history_list.addItem(item)

        history_list.itemDoubleClicked.connect(self.open_history_item)
        layout.addWidget(history_list)

        history_dialog.setLayout(layout)
        history_dialog.exec_()

    def open_history_item(self, item):
        url = item.text()
        self.load_url(self.tab_widget.currentWidget(), url)

    def open_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle(translations[self.language]["settings_title"])
        settings_dialog.setModal(True)

        layout = QVBoxLayout()

        language_label = QLabel(translations[self.language]["language_label"])
        layout.addWidget(language_label)

        language_combo = QComboBox()
        language_combo.addItem("English")
        language_combo.addItem("Deutsch")
        language_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(language_combo)

        search_engine_label = QLabel("Search Engine:")
        layout.addWidget(search_engine_label)

        search_engine_combo = QComboBox()
        search_engine_combo.addItem("Google")
        search_engine_combo.addItem("Edge")
        search_engine_combo.addItem("DuckDuckGo")

        current_search_engine_index = 0 
        if self.search_engine == "Edge":
            current_search_engine_index = 1
        elif self.search_engine == "DuckDuckGo":
            current_search_engine_index = 2

        search_engine_combo.setCurrentIndex(current_search_engine_index)
        search_engine_combo.currentIndexChanged.connect(self.change_search_engine)
        layout.addWidget(search_engine_combo)

        save_btn = QPushButton(translations[self.language]["save_btn"])
        save_btn.clicked.connect(settings_dialog.close)
        layout.addWidget(save_btn)

        settings_dialog.setLayout(layout)
        settings_dialog.exec_()

    def change_search_engine(self, index):
        if index == 0:
            self.search_engine = "Google"
        elif index == 1:
            self.search_engine = "Edge"
        elif index == 2:
            self.search_engine = "DuckDuckGo"

    def navigate(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            url = self.url_bar.text()
            if "." not in url:
                search_engine_url = self.get_search_engine_url()
                url = search_engine_url + url.replace(" ", "+")
            elif not url.startswith("https://") and not url.startswith("http://"):
                url = "https://" + url
            self.load_url(current_tab, url)
            self.history.append(url)

    def get_search_engine_url(self):
        if self.search_engine == "Google":
            return "https://www.google.com/search?q="
        elif self.search_engine == "Edge":
            return "https://www.bing.com/search?q="
        elif self.search_engine == "DuckDuckGo":
            return "https://duckduckgo.com/?q="

    def change_language(self, index):
        if index == 0:
            self.language = "en"
        elif index == 1:
            self.language = "de"

        self.setWindowTitle(translations[self.language]["window_title"])
        self.go_btn.setText(translations[self.language]["go_btn"])
        self.back_btn.setText(translations[self.language]["back_btn"])
        self.forward_btn.setText(translations[self.language]["forward_btn"])
        self.new_tab_btn.setText(translations[self.language]["new_tab_btn"])
        self.bookmark_btn.setText(translations[self.language]["bookmark_btn"])
        self.settings_btn.setText(translations[self.language]["settings_btn"])
        self.history_btn.setText(translations[self.language]["history_btn"])

        self.settings_btn.setText(translations[self.language]["settings_btn"])
        self.history_btn.setText(translations[self.language]["history_btn"])

    def show_bookmarks(self):
        bookmarks_dialog = QDialog(self)
        bookmarks_dialog.setWindowTitle("Bookmarks")
        bookmarks_dialog.setModal(True)

        layout = QVBoxLayout()

        bookmarks_list = QListWidget()
        for bookmark in self.bookmarks:
            title = bookmark["title"]
            url = bookmark["url"]

            item = QListWidgetItem()
            item.setText(f"<b>{title}</b>: {url}")
            item.setTextAlignment(Qt.AlignLeft)
            item.setFlags(item.flags() | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)

            bookmarks_list.addItem(item)

        bookmarks_list.itemDoubleClicked.connect(self.open_bookmark)
        layout.addWidget(bookmarks_list)

        bookmarks_dialog.setLayout(layout)
        bookmarks_dialog.exec_()


    def open_bookmark(self, item):
        bookmark_text = item.text()
        bookmark_url = bookmark_text.split(": ")[1]
        self.load_url(self.tab_widget.currentWidget(), bookmark_url)


    def closeEvent(self, event):
        result = QMessageBox.question(self, "Exit Confirmation", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
class CustomWebView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event):
        menu = QMenu(self)


        action1 = menu.addAction("Aktion 1")
        action2 = menu.addAction("Aktion 2")

        menu.exec_(event.globalPos())


if __name__ == "__main__":
    app = QApplication([])
    browser = Browser()
    browser.showMaximized()
    app.exec_() 
