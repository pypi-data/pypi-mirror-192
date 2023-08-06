from lxml.etree import fromstring


class WebElement:
    def __init__(self, srv_addr, session, tab_id, xpath, html):
        self.srv_addr = srv_addr
        self.session = session
        self.tab_id = tab_id
        self.xpath = xpath
        self.html = fromstring(html) if type(html) == str else html

    def find_element(self, xpath, remote=True):
        els = self.html.xpath(xpath)
        return WebElement(
            srv_addr=self.srv_addr,
            session=self.session,
            tab_id=self.tab_id,
            xpath=xpath,
            html=els[0]
        )

    def find_elements(self, xpath, remote=True):
        els = self.html.xpath(xpath)
        web_els = []
        for el in els:
            web_els.append(
                WebElement(
                    srv_addr=self.srv_addr,
                    session=self.session,
                    tab_id=self.tab_id,
                    xpath=xpath,
                    html=el
                )
            )
        return web_els

    def get_attribute(self, attribute_name):
        return self.html.get(attribute_name)

    @property
    def text(self):
        return self.html.text

    def screenshot(self):
        pass

    def click(self):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.html.tag}>"
