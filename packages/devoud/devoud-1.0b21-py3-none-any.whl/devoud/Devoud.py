#!/usr/bin/python3
from pyshortcuts import make_shortcut  # ставить всегда первым, иначе ошибка в windows системах
from devoud.browser import *
from devoud.browser.filesystem import FileSystem
from devoud.browser.main_window import BrowserWindow
from devoud.browser.pages import is_url
from devoud.browser.update import update


def main():
    start_time = time.perf_counter()
    from devoud import __version__
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            return print('Использование:       devoud [ссылка/опция]\n\n'
                         'Доступные опции:\n'
                         ' devoud              запуск браузера\n'
                         ' devoud \'ссылка\'     запустить браузер и открыть ссылку в новой вкладке\n'
                         ' devoud help         помощь по командам\n'
                         ' devoud update       проверить и установить обновления\n'
                         ' devoud version      показать текущую версию браузера\n'
                         ' devoud shortcut     создать ярлык запуска')
        elif sys.argv[1] == 'version':
            return print(f'Devoud ({__version__}) by OneEyedDancer')
        elif sys.argv[1] == 'update':
            update()
        elif sys.argv[1] == 'shortcut':
            FileSystem.create_launch_shortcut()
            return

    print(fr'''---------------------------------------------
  Добро пожаловать в
  _____  ________      ______  _    _ _____  
 |  __ \|  ____\ \    / / __ \| |  | |  __ \ 
 | |  | | |__   \ \  / / |  | | |  | | |  | |
 | |  | |  __|   \ \/ /| |  | | |  | | |  | |
 | |__| | |____   \  / | |__| | |__| | |__| |
 |_____/|______|   \/   \____/ \____/|_____/ 
    ({__version__}) by OneEyedDancer            
---------------------------------------------''')
    os.environ["QT_FONT_DPI"] = "96"
    if platform == 'wind32':
        sys.argv += ['-platform', 'windows:darkmode=2']
    app = QApplication(sys.argv)

    window = BrowserWindow()

    if len(sys.argv) > 1:
        if is_url(sys.argv[1]):
            # открытие ссылки в новой вкладке
            window.tab_widget.create_tab(sys.argv[1])

    size = window.screen().availableGeometry()
    window.resize(size.width() * 2 / 3, size.height() * 2 / 3)
    window.show()
    window.change_style()

    print(f'[Время]: Запуск занял {time.perf_counter()-start_time:.4f} секунд')
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
