from devoud.browser import *


class Settings:
    filename = 'settings.json'
    default = {"saveHistory": False,
               "restoreSession": False,
               "adblock": True,
               "cookies": True,
               "javascript": True,
               "systemWindowFrame": False,
               "theme": "night",
               "homePage": "ya.ru",
               "searchEngine": "Yandex",
               "newPage": "Заставка с часами",
               "TabBarPosition": "Сверху"}

    def __init__(self, parent):
        self.parent = parent
        self.FS = parent.FS
        self._dict = {}
        with Path(self.FS.user_dir(), self.filename).open() as settings_file:
            try:
                self._dict = json.load(settings_file)
            except json.decoder.JSONDecodeError:
                print(f'[Закладки]: Произошла ошибка при чтении {self.filename}, ошибка: {json.decoder.JSONDecodeError}')
                self.restore()

    def settings(self) -> dict:
        return self._dict

    def set(self, option, arg=None):
        """Если arg не установлен, то значение инвертируется"""
        if arg is None:
            try:
                self._dict[option] = not self._dict[option]
            except KeyError:
                try:
                    self._dict[option] = not self.default[option]
                except KeyError:
                    return print(f'[Настройки]: Параметра {option} не существует в настройках!')
        else:
            self._dict[option] = arg
        with Path(self.FS.user_dir(), self.filename).open('w') as settings_file:
            json.dump(self._dict, settings_file, indent=4, ensure_ascii=False)

    def get(self, option):
        try:
            return self._dict.get(option, self.default[option])
        except KeyError:
            print(f'[Настройки]: Параметра {option} не существует в настройках!')
            return None

    def restore(self) -> None:
        print('[Настройки]: Идёт восстановление настроек')
        self._dict = self.default
        with Path(self.FS.user_dir(), self.filename).open('w') as settings_file:
            json.dump(self._dict, settings_file, indent=4, ensure_ascii=False)

