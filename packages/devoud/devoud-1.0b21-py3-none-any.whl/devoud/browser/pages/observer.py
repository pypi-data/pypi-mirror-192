import devoud.browser.pages as pages


class PagesObserver:
    _pages = []

    @classmethod
    def pages(cls):
        return cls._pages

    @classmethod
    def urls(cls):
        return list(map(lambda page: page.url, cls._pages))

    @classmethod
    def add_page(cls, page, index=-1):
        cls._pages.insert(index, page)

    @classmethod
    def remove_page(cls, page):
        cls._pages.remove(page)

    @classmethod
    def update_control_pages(cls):
        for page in cls._pages:
            if isinstance(page.view, pages.ControlPage):
                page.reload()
