# -*- coding: utf-8 -*-

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


LOCATOR_MAP = {
    'class_name': By.CLASS_NAME,
    'css': By.CSS_SELECTOR,
    'id': By.ID,
    'link_text': By.LINK_TEXT,
    'name': By.NAME,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'xpath': By.XPATH
}


class PageObject(object):
    """ Page Object pattern."""

    def __init__(self, webdriver, root_uri=None):
        self.webdriver = webdriver
        self.root_uri = root_uri if root_uri else getattr(
            webdriver, 'root_uri', None)

    def get(self, uri):
        root_uri = self.root_uri or ''
        self.webdriver.get(root_uri + uri)

    def wait_for_page_by_title(self, title, timeout=30):
        WebDriverWait(self.webdriver, timeout).until(
            lambda driver: EC.title_is(title) and driver.execute_script(
                "return document.readyState == 'complete';"),
            'Page load time with title "%s" has expired' % title)

    @property
    def title(self):
        return self.webdriver.title


class PageElementError(Exception):
    pass


class PageElementInterace(object):
    """ Wrapper over the WebElement."""

    def __init__(self, webelement, locator):
        self._el = webelement
        self._locator = locator

    def __getattr__(self, attr):
        return getattr(self._el, attr)

    @property
    def webelement(self):
        return self._el

    @property
    def enabled(self):
        return self._el.is_enabled()

    @property
    def disabled(self):
        return not self.enabled

    @property
    def value(self):
        return self._el.get_attribute('value')

    @property
    def visible(self):
        return self._el.is_displayed()


class PageElement(object):
    """ Page Element descriptor."""

    TIMEOUT = 10

    def __init__(self, **locator):
        if not locator:
            raise ValueError("Please specify a locator")
        if len(locator) > 1:
            raise ValueError("Please specify only one locator")
        key, value = next(iter(locator.items()))
        self._locator = (LOCATOR_MAP[key], value)

    def find(self, webdriver):
        return WebDriverWait(webdriver, PageElement.TIMEOUT).until(
            lambda d: d.find_element(*self._locator),
            "Not found element by %s: <%s>" % self._locator)

    def __get__(self, instance, owner):
        try:
            logging.info("Looking for element by %s: <%s>", *self._locator)
            return PageElementInterace(
                self.find(instance.webdriver), self._locator)
        except AttributeError:
            pass

    def __set__(self, instance, value):
        pass


class PageElements(PageElement):
    """ Like `PageElement` but returns multiple results."""

    def find(self, webdriver):
        return WebDriverWait(webdriver, PageElement.TIMEOUT).until(
            lambda d: d.find_elements(*self._locator),
            "Not found elements by %s: <%s>" % self._locator)
