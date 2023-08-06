import requests

from chrome_boss.element import WebElement


class ChromeTab:
    def __init__(self, srv_addr, tab_id, url, title, session):
        self.srv_addr = srv_addr
        self.id = tab_id
        self.url = url
        self.title = title
        self.session = session

    def get(self, url):
        resp = requests.post(f"{self.srv_addr}/tab/get", json={
            "session": self.session,
            "tab": self.id,
            "url": url
        })
        if resp.status_code == 200:
            data = resp.json()
            self.url = url
            self.title = data.get('title')
        else:
            raise ValueError(f"status code: {resp.status_code}")

    def find_element(self, xpath):
        resp = requests.post(f"{self.srv_addr}/tab/find_element", json={
            "session": self.session,
            "tab": self.id,
            "xpath": xpath
        })
        data = resp.json()
        assert self.session == data.get('session')
        assert self.url == data.get('url')
        assert self.title == data.get('title')
        assert self.id == data.get('tab')
        html = data.get('html')
        assert html
        return WebElement(
            srv_addr=self.srv_addr,
            session=self.session,
            tab_id=self.id,
            xpath=xpath,
            html=html
        )

    @property
    def screenshot(self):
        resp = requests.post(f"{self.srv_addr}/tab/screenshot", json={
            "session": self.session,
            "tab": self.id,
        })
        data = resp.json()
        assert self.session == data.get('session')
        assert self.url == data.get('url')
        assert self.title == data.get('title')
        assert self.id == data.get('tab')
        return data.get('screenshot')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<Tab: {self.title}>"
