from devoud.browser import *


class Session:
    filename = 'session.json'

    def __init__(self, parent):
        self.parent = parent
        self.FS = parent.FS
        self._dict = {}
        with Path(self.FS.user_dir(), self.filename).open() as session_file:
            try:
                self._dict = json.load(session_file)
            except Exception as error:
                print(
                    f'[Вкладки]: Произошла ошибка при чтении {self.filename}, ошибка: {error}')
                self.restore_file()

    def restore(self):
        if self.parent.settings.get('restoreSession') and self._dict:
            try:
                self.parent.tab_widget.currentChanged.disconnect()
                for key, data in self._dict.items():
                    if key.isdigit():
                        self.parent.tab_widget.create_tab(url=data['url'],
                                                          title=data['title'],
                                                          page_history=data['pages'],
                                                          page_history_position=data['pages_position'],
                                                          save_page_history=False,
                                                          switch=False,
                                                          load=False)
                self.parent.tab_widget.setCurrentIndex(self._dict['lastPage'])
                self.parent.tab_widget.current().load()
                self.parent.tab_widget.currentChanged.connect(self.parent.tab_widget.tab_changed)
                print('[Вкладки]: Предыдущая сессия восстановлена')
            except Exception as error:
                print(f'[Вкладки]: Не удалось восстановить прошлую сессию, ошибка {error}')
                self.parent.load_home_page()
        else:
            self.parent.load_home_page()

    def save(self):
        if self.parent.settings.get('restoreSession'):
            self._dict = {}
            for tab_index in range(self.parent.tab_widget.count()):
                page = self.parent.tab_widget.widget(tab_index)
                self._dict[str(tab_index)] = {
                    'url': page.url,
                    'title': page.title,
                    'pages': page.page_history,
                    'pages_position': page.page_history_position
                }
            self._dict['lastPage'] = self.parent.tab_widget.currentIndex()
            with Path(self.parent.FS.user_dir(), self.filename).open('w') as session_file:
                try:
                    json.dump(self._dict, session_file, sort_keys=True, indent=4, ensure_ascii=False)
                except Exception as error:
                    print(f'[Вкладки]: Произошла ошибка при записи данных в {self.filename}, ошибка {error}')
                else:
                    return print('[Вкладки]: Текущая сессия сохранена')
        print('[Вкладки]: Текущая сессия не сохранена')

    def restore_file(self):
        print('[Вкладки]: Идёт восстановление файла сессии')
        self._dict = {}
        with Path(self.FS.user_dir(), self.filename).open('w') as session_file:
            json.dump(self._dict, session_file, indent=4, ensure_ascii=False)
