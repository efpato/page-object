# -*- coding: utf-8 -*-

import logging

from page_object import PageElement, PageElementError, PageElementWrapper

__all__ = ['Select', 'SelectWrapper']

logger = logging.getLogger(__name__)


class SelectWrapper(PageElementWrapper):
    """ Wrapper for <select>"""

    @property
    def options(self):
        logger.info("%r getting options ...", self)
        return self._el.find_elements_by_tag_name('option')

    @property
    def text(self):
        logger.info("%r getting text ...", self)
        ret = None
        for option in self.options:
            if option.is_selected():
                ret = option.text
        return ret

    @property
    def value(self):
        logger.info("%r getting value ...", self)
        ret = None
        for option in self.options:
            if option.is_selected():
                ret = option.get_attribute('value')
        return ret

    def select_by_text(self, text):
        logger.info('%r selecting by text "%s" ...', self, text)
        for option in self.options:
            if option.text.strip() == text:
                option.click()
                return
        raise PageElementError('%r has no option with text "%s"' % (
            self, text))

    def select_by_value(self, value):
        logger.info('%r selecting by value "%s" ...', self, value)
        for option in self.options:
            if option.get_attribute('value') == value:
                option.click()
                return
        raise PageElementError('%r has no option with value "%s"' % (
            self, value))


class Select(PageElement):
    """ Select descriptor"""

    def __get__(self, instance, owner):
        el = SelectWrapper(self.find(instance.webdriver), self._locator)
        el.move_to_self()
        return el

    def __set__(self, instance, value):
        if value is None:
            return

        value = str(value).strip()
        if not value:
            return

        self.__get__(instance, instance.__class__).select_by_text(value)
