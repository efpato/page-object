# -*- coding: utf-8 -*-

import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException


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

SCREENSHOTS_DIR = 'screenshots'


class PageObject(object):
    """Page Object pattern."""

    def __init__(self, webdriver, root_uri=None):
        self.webdriver = webdriver
        self.root_uri = root_uri if root_uri else getattr(webdriver, 'root_uri', None)

    def get(self, uri):
        root_uri = self.root_uri or ''
        self.webdriver.get(root_uri + uri)

    @property
    def title(self):
        return self.webdriver.title


class PageElementError(Exception): pass


class PageElement(object):
    """Page Element descriptor."""

    TIMEOUT = 10

    def __init__(self, **locator):
        if not locator:
            raise ValueError("Please specify a locator")
        if len(locator) > 1:
            raise ValueError("Please specify only one locator")
        key, value = next(iter(locator.items()))
        self._locator = (LOCATOR_MAP[key], value)

    def find(self, webdriver):
        try:
            return WebDriverWait(webdriver, PageElement.TIMEOUT).until(
                lambda d: d.find_element(*self._locator),
                'Didn\'t find element by %s="%s".' % self._locator)
        except TimeoutException as e:
            if not os.path.exists(SCREENSHOTS_DIR):
                os.mkdir(SCREENSHOTS_DIR)
            png = '%s/%s.png' % (SCREENSHOTS_DIR, time.time())
            webdriver.save_screenshot(png)
            e.msg += ' See %s' % png
            raise e

    def __get__(self, instance, owner):
        try:
            return self.find(instance.webdriver)
        except AttributeError:
            return

    def __set__(self, instance, value):
        raise NotImplemented()


class PageElements(PageElement):
    """Like `PageElement` but returns multiple results."""

    def find(self, webdriver):
        try:
            return WebDriverWait(webdriver, PageElement.TIMEOUT).until(
                lambda d: d.find_elements(*self._locator),
                'Didn\'t find elements by %s="%s".' % self._locator)
        except TimeoutException as e:
            if not os.path.exists(SCREENSHOTS_DIR):
                os.mkdir(SCREENSHOTS_DIR)
            png = '%s/%s.png' % (SCREENSHOTS_DIR, time.time())
            webdriver.save_screenshot(png)
            e.msg += ' See %s' % png
            raise e
