from devoud.browser import *
from devoud.browser.styles.theme import Theme
from devoud.browser.web.adblocker.ad_blocker import AdBlocker, RequestInterceptor
from devoud.browser.web.search_engines import search_engines
from devoud.browser.widgets.address_panel import AddressPanel
from devoud.browser.filesystem import FileSystem
from devoud.browser.widgets.find_on_page import FindWidget
from devoud.browser.download_manager import DownloadManager
from devoud.browser.pages.observer import PagesObserver
from devoud.browser.widgets.tab_widget import BrowserTabWidget
from devoud.browser.widgets.title_bar import TitleBar
from devoud.browser.settings import Settings
from devoud.browser.bookmarks import Bookmarks
from devoud.browser.history import History
from devoud.browser.session import Session
import devoud


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.FS = FileSystem()
        self.settings = Settings(self)
        self.session = Session(self)
        self.history = History(self)
        self.bookmarks = Bookmarks(self)
        self.theme = Theme(self)

        self.new_page_dict = {'Заставка с часами': lambda: 'https://web.tabliss.io/',
                              'Поисковик': lambda: search_engines[self.settings.get('searchEngine')][1],
                              'Домашняя страница': lambda: QUrl.fromUserInput(
                                  self.settings.get('homePage')).toString()}
        self.new_page = self.new_page_dict.get(self.settings.get('newPage'))()
        self.systemFrame = self.settings.get('systemWindowFrame')

        app_icons = {'linux': 'icons:devoud.svg',
                     'win32': 'icons:devoud.ico',
                     'darwin': 'icons:devoud.icns'}
        self.setWindowIcon(QIcon(app_icons.get(platform, 'icons:devoud.png')))
        self.setWindowTitle(__name__)
        self.setMinimumSize(QSize(400, 300))

        # профиль для веб-страниц
        self.profile = QWebEngineProfile('DevoudProfile')
        self.profile.setPersistentStoragePath(f'{self.FS.user_dir()}/web_profile')
        self.profile.setCachePath(f'{self.FS.user_dir()}/cache')
        self.download_manager = DownloadManager(self)
        self.profile.downloadRequested.connect(lambda req: self.download_manager.download_requested(req))

        # блокировщик рекламы
        self.ad_blocker = AdBlocker(self)
        if self.ad_blocker.is_enable():
            self.ad_blocker.add_rules()
            self.interceptor = RequestInterceptor(self.ad_blocker.rules)
            self.profile.setUrlRequestInterceptor(self.interceptor)

        # шрифт
        QFontDatabase.addApplicationFont('./ui/fonts/ClearSans-Medium.ttf')
        self.setFont(QFont('Clear Sans Medium'))

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.window_layout = QGridLayout(self.central_widget)
        self.window_layout.setSpacing(0)
        self.window_layout.setContentsMargins(0, 0, 0, 0)

        # для растяжения окна с кастомной рамкой
        self.size_grip_right = QSizeGrip(self)
        self.window_layout.addWidget(self.size_grip_right, 1, 2)
        self.size_grip_right.setFixedWidth(5)
        self.size_grip_right.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.size_grip_right.setStyleSheet('border-radius: 5px; background: transparent;')

        self.size_grip_left = QSizeGrip(self)
        self.size_grip_left.setFixedWidth(5)
        self.size_grip_left.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.window_layout.addWidget(self.size_grip_left, 1, 0)
        self.size_grip_left.setStyleSheet('border-radius: 5px; background: transparent;')

        self.size_grip_top = QSizeGrip(self)
        self.window_layout.addWidget(self.size_grip_top, 0, 1)
        self.size_grip_top.setFixedHeight(5)
        self.size_grip_top.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.size_grip_top.setStyleSheet('border-radius: 5px; background: transparent;')

        self.size_grip_bottom = QSizeGrip(self)
        self.window_layout.addWidget(self.size_grip_bottom, 2, 1)
        self.size_grip_bottom.setFixedHeight(5)
        self.size_grip_bottom.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.size_grip_bottom.setStyleSheet('border-radius: 5px; background: transparent;')

        # все кроме size grip
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName('main_frame')

        # ломается рендер веб-страниц
        # self.window_shadow = QGraphicsDropShadowEffect(self)
        # self.window_shadow.setBlurRadius(17)
        # self.window_shadow.setXOffset(0)
        # self.window_shadow.setYOffset(0)
        # self.window_shadow.setColor(QColor(0, 0, 0, 150))
        # self.main_frame.setGraphicsEffect(self.window_shadow)

        self.window_layout.addWidget(self.main_frame, 1, 1)
        self.main_layout = QGridLayout(self.main_frame)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # адресная панель
        self.address_panel = AddressPanel(self)
        self.main_layout.addWidget(self.address_panel, 1, 0, 1, 1)
        self.address_line_edit = self.address_panel.address_line_edit
        self.add_tab_button = self.address_panel.add_tab_button

        # виджет вкладок
        self.main_layout.addWidget(self.tab_widget, 3, 0)
        self.tab_widget.set_tab_bar_position()

        # кастомная рамка окна
        self.title_bar = TitleBar(self)
        self.main_layout.addWidget(self.title_bar, 0, 0)
        self.title_bar.close_button.clicked.connect(self.close)
        self.title_bar.maximize_button.clicked.connect(self.restore_or_maximize)
        self.title_bar.hide_button.clicked.connect(self.showMinimized)

        def move_window(event):
            if self.isMaximized():
                self.restore_or_maximize()
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.title_bar.mouseMoveEvent = move_window

        # выбор рамки окна
        if not self.systemFrame:
            # убрать системную рамку окна
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.window_corner_radius('12px')
        else:
            self.title_bar.deleteLater()
            self.size_grip_right.deleteLater()
            self.size_grip_left.deleteLater()
            self.size_grip_top.deleteLater()
            self.size_grip_bottom.deleteLater()

        # комбинации клавиш
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.update_page)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.show_find_on_page)
        QShortcut(QKeySequence("Alt+H"), self).activated.connect(lambda: self.load_home_page(new_tab=False))
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(
            lambda: self.tab_widget.create_tab(self.new_page))
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(
            lambda: self.bookmarks.append(self.tab_widget.current().data()))
        QShortcut(QKeySequence("Ctrl+Shift+O"), self).activated.connect(
            lambda: self.tab_widget.create_tab('devoud://control#bookmarks'))
        QShortcut(QKeySequence("Ctrl+H"), self).activated.connect(
            lambda: self.tab_widget.create_tab('devoud://control#history'))
        QShortcut(QKeySequence("Ctrl+J"), self).activated.connect(
            lambda: self.tab_widget.create_tab('devoud://control#downloads'))
        QShortcut(QKeySequence("Ctrl+W"), self).activated.connect(
            lambda: self.tab_widget.close_tab(self.tab_widget.currentIndex()))
        QShortcut(QKeySequence("Alt+Left"), self).activated.connect(self.back_page)
        QShortcut(QKeySequence("Alt+Right"), self).activated.connect(self.forward_page)

        # восстановление предыдущей сессии
        self.session.restore()

    def change_style(self, name=None):
        self.theme = Theme(self, name)
        self.setStyleSheet(self.theme.style())
        self.address_line_edit.findChild(QToolButton).setIcon(QIcon('custom:close(address_line_frame).svg'))

    def window_corner_radius(self, radius):
        self.main_frame.setStyleSheet(Template("""
        #main_frame { 
            border-radius: $radius;
        }""").substitute(radius=radius))

    def show_find_on_page(self):
        page = self.tab_widget.current()
        page_find_widget = page.findChild(FindWidget)
        if page_find_widget:
            if not page_find_widget.isHidden():
                page_find_widget.hide_find()
            else:
                page_find_widget.show()
                page_find_widget.find_focus()
                page_find_widget.find_text()
        elif not page.view.embedded:
            find_widget = FindWidget(page)
            page.layout().addWidget(find_widget)
            find_widget.show()
            find_widget.find_focus()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def restore_or_maximize(self):
        if self.isMaximized():
            self.window_corner_radius('12px')
            self.showNormal()
        else:
            self.window_corner_radius('0px')
            self.showMaximized()

    def load_home_page(self, new_tab=True):
        if new_tab:
            self.tab_widget.create_tab()
        self.tab_widget.current().load(self.settings.get('homePage'))

    def set_title(self, text):
        self.setWindowTitle(f"{text} – {devoud.__name__} {devoud.__version__}")
        if not self.systemFrame:
            self.title_bar.label.setText(f"{text} – {devoud.__name__} {devoud.__version__}")

    def back_page(self):
        self.tab_widget.current().back()

    def forward_page(self):
        self.tab_widget.current().forward()

    def stop_load_page(self):
        self.tab_widget.current().stop()

    def update_page(self):
        self.tab_widget.current().reload()

    def closeEvent(self, event):
        self.session.save()
        for page in PagesObserver.pages():
            page.deleteLater()
        super().closeEvent(event)

    def restart(self):
        self.session.save()
        os.execv(sys.executable, ['python'] + sys.argv)

    @cached_property
    def tab_widget(self):
        return BrowserTabWidget()
