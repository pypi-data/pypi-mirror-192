from devoud.browser import *
from devoud.browser.widgets.context_menu import BrowserContextMenu
from devoud.browser.download_manager import DownloadMethod
from devoud.browser.web.search_engines import search_engines
from devoud.browser.pages import is_url


class BrowserWebView(QWebEngineView):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.FS = parent.window().FS
        self.profile = parent.window().profile
        self.setAutoFillBackground(True)
        self.embedded = False
        self.title = '. . .'
        self.setPage(QWebEnginePage(self.window().profile, self))
        self.dev_view = None

        QShortcut(QKeySequence("F11"), self).activated.connect(self.toggle_fullscreen)
        QShortcut(QKeySequence("F12"), self).activated.connect(self.toggle_dev_tools)

    def is_loading(self):
        return self.page().isLoading()

    def inspect_page(self):
        if self.dev_view is None:
            self.dev_view = QWebEngineView()
            self.parent.view_spliter.addWidget(self.dev_view)
            self.parent.view_spliter.setSizes([200, 100])
            self.page().setDevToolsPage(self.dev_view.page())
        if self.dev_view.isHidden():
            self.dev_view.show()
        self.page().triggerAction(QWebEnginePage.InspectElement)

    def toggle_dev_tools(self):
        if self.dev_view is None:
            self.dev_view = QWebEngineView()
            self.parent.view_spliter.addWidget(self.dev_view)
            self.parent.view_spliter.setSizes([200, 100])
            self.page().setDevToolsPage(self.dev_view.page())
        elif self.dev_view.isVisible():
            self.dev_view.hide()
        else:
            self.dev_view.show()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.parent.view_spliter.addWidget(self)
            self.showNormal()
            self.window().show()
        else:
            self.window().hide()
            self.setParent(None)
            self.showFullScreen()

    def save_image_as(self):
        DownloadMethod.Method = DownloadMethod.SaveAs
        self.page().triggerAction(QWebEnginePage.DownloadImageToDisk)

    def createWindow(self, type_):
        if type_ == QWebEnginePage.WebBrowserTab:
            # запрос на новую вкладку
            return self.window().tab_widget.create_tab(end=False)

    def contextMenuEvent(self, event):
        menu = BrowserContextMenu(self.window())
        page = self.page()
        page_request = self.lastContextMenuRequest()
        edit_flags = page_request.editFlags()
        media_flags = page_request.mediaFlags()
        link = None

        if media_flags:
            media_url = self.lastContextMenuRequest().mediaUrl().toString()
            menu.addAction('Копировать изображение',
                           lambda: page.triggerAction(QWebEnginePage.CopyImageToClipboard))
            menu.addAction('Копировать ссылку на изображение',
                           lambda: page.triggerAction(QWebEnginePage.CopyImageUrlToClipboard))
            menu.addAction('Сохранить изображение как', self.save_image_as)
            menu.addAction('Открыть в новой вкладке',
                           lambda: self.window().tab_widget.create_tab(media_url, switch=False, end=False))
        elif edit_flags:
            if is_url(page_request.linkUrl().toString()):
                link = page_request.linkUrl().toString()
            elif is_url(page_request.selectedText()):
                link = page_request.selectedText()
            if link:
                menu.addAction('Копировать ссылку', lambda: page.triggerAction(QWebEnginePage.CopyLinkToClipboard))
                menu.addAction('Открыть в новой вкладке',
                               lambda: self.window().tab_widget.create_tab(link, switch=False, end=False))
            if QWebEngineContextMenuRequest.CanCopy in edit_flags:
                menu.addAction('Копировать', lambda: page.triggerAction(QWebEnginePage.Copy))
            if QWebEngineContextMenuRequest.CanPaste in edit_flags:
                menu.addAction('Вставить', lambda: page.triggerAction(QWebEnginePage.Paste))
            if QWebEngineContextMenuRequest.CanCut in edit_flags:
                menu.addAction('Вырезать', lambda: page.triggerAction(QWebEnginePage.Cut))
            if QWebEngineContextMenuRequest.CanUndo in edit_flags:
                menu.addAction('Отменить', lambda: page.triggerAction(QWebEnginePage.Undo))
            if QWebEngineContextMenuRequest.CanRedo in edit_flags:
                menu.addAction('Повторить', lambda: page.triggerAction(QWebEnginePage.Redo))
            if QWebEngineContextMenuRequest.CanSelectAll in edit_flags:
                menu.addAction('Выделить всё', lambda: page.triggerAction(QWebEnginePage.SelectAll))
            if QWebEngineContextMenuRequest.CanCopy in edit_flags:
                menu.addSeparator()
                menu.addAction(f'Поиск в {self.window().settings.get("searchEngine")}',
                               lambda: self.window().tab_widget.create_tab(
                                   f'{search_engines[self.window().settings.get("searchEngine")][0]}{page.selectedText()}'))
        menu.addSeparator()
        menu.addAction('Назад', self.back)
        menu.addAction('Вперед', self.forward)
        menu.addAction('Перезагрузить', lambda: page.triggerAction(QWebEnginePage.Reload))
        menu.addSeparator()
        menu.addAction('Инспектировать', self.inspect_page)
        menu.addAction('Исходный код', lambda: page.triggerAction(QWebEnginePage.ViewSource))
        menu.popup(event.globalPos())
