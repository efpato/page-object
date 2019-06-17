# -*- coding: utf-8 -*-

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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

logger = logging.getLogger(__name__)


class PageObject(object):
    """ Page Object pattern"""

    def __init__(self, webdriver, root_uri=None):
        logger.info("Creating %s ...", self.__class__.__name__)
        self.webdriver = webdriver
        self.root_uri = root_uri if root_uri else getattr(
            webdriver, 'root_uri', None)

    def get(self, uri):
        root_uri = self.root_uri or ''
        logger.info("Getting url %s ...", root_uri + uri)
        self.webdriver.get(root_uri + uri)

    def wait_for_page_by_title(self, title, timeout=30):
        logger.info("Waiting for page title `%s` [timeout=%d] ...",
                    title, timeout)
        WebDriverWait(self.webdriver, timeout).until(
            lambda d: EC.title_is(title)(d) and d.execute_script(
                "return document.readyState == 'complete';"),
            'Page load time with title "%s" has expired' % title)

    @property
    def title(self):
        return self.webdriver.title


class PageElementError(Exception):
    pass


class PageElementWrapper(object):
    """ Wrapper for PageElement"""

    def __init__(self, webelement, locator):
        self._el = webelement
        self._locator = locator

    def __repr__(self):
        return '%s(%s="%s")' % (self.__class__.__name__, *self._locator)

    def __getattr__(self, attr):
        return getattr(self._el, attr)

    @property
    def webelement(self):
        return self._el

    @property
    def enabled(self):
        logger.info("%r is enabled ...", self)
        return self._el.is_enabled()

    @property
    def disabled(self):
        logger.info("%r is disabled ...", self)
        return not self.enabled

    @property
    def value(self):
        logger.info("%r getting value ...", self)
        return self._el.get_attribute('value')

    @property
    def inner_html(self):
        logger.info("%r getting innerHTML ...", self)
        return self._el.get_attribute('innerHTML')

    @property
    def visible(self):
        logger.info("%r is visible ...", self)
        return self._el.is_displayed()

    def move_to_self(self):
        logger.info("%r moving to element ...", self)
        ActionChains(self._el.parent).move_to_element(self._el).perform()

    def wait_for_clickability(self, timeout=10):
        logger.info("Waiting for clickability %r ...", self)
        WebDriverWait(self._el.parent, timeout).until(
            EC.element_to_be_clickable(self._locator),
            'Waiting for clickability %s has expired!' % self)

    def wait_for_visibility(self, timeout=10):
        logger.info("Waiting for visibility %r ...", self)
        WebDriverWait(self._el.parent, timeout).until(
            EC.visibility_of_element_located(self._locator),
            'Waiting for visibility %s has expired!' % self)

    def wait_for_invisibility(self, timeout=10):
        logger.info("Waiting for invisibility %r ...", self)
        WebDriverWait(self._el.parent, timeout).until(
            EC.invisibility_of_element_located(self._locator),
            'Waiting for invisibility %s has expired!' % self)


class PageElement(object):
    """ PageElement descriptor"""

    TIMEOUT = 10

    def __init__(self, **locator):
        if not locator:
            raise ValueError("Please specify a locator")
        if len(locator) > 1:
            raise ValueError("Please specify only one locator")
        key, value = next(iter(locator.items()))
        self._locator = (LOCATOR_MAP[key], value)

    def find(self, webdriver):
        logger.info('Looking for element by <%s="%s">', *self._locator)
        return WebDriverWait(webdriver, self.TIMEOUT).until(
            lambda d: d.find_element(*self._locator),
            'Not found element by <%s="%s">' % self._locator)

    def __get__(self, instance, owner):
        el = PageElementWrapper(self.find(instance.webdriver), self._locator)
        el.move_to_self()
        return el

    def __set__(self, instance, value):
        pass


class PageElements(PageElement):
    """ Like `PageElement` but returns multiple results"""

    TIMEOUT = 10

    def find(self, webdriver):
        logger.info('Looking for elements by <%s="%s">', *self._locator)
        return WebDriverWait(webdriver, self.TIMEOUT).until(
            lambda d: d.find_elements(*self._locator),
            'Not found elements by <%s="%s">' % self._locator)

    def __get__(self, instance, owner):
        ret = []
        for webelement in self.find(instance.webdriver):
            ret.append(PageElementWrapper(webelement, self._locator))
        return ret
