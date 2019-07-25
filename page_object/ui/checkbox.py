# -*- coding: utf-8 -*-

import logging

from page_object import PageElement, PageElementWrapper

__all__ = ['Checkbox', 'CheckboxWrapper']

logger = logging.getLogger(__name__)


class CheckboxWrapper(PageElementWrapper):
    """ Wrapper for <input type="checkbox">"""
    @property
    def checked(self):
        logger.info("%r is checked ...", self)
        return self._el.is_selected()

    def check(self, timeout=0):
        if self.checked:
            logging.info("%r is already checked", self)
            return

        if timeout:
            self.wait_for_clickability(timeout)

        logger.info("%r clicking ...", self)
        self._el.click()

    def uncheck(self, timeout=0):
        if not self.checked:
            logging.info("%r is already unchecked", self)
            return

        if timeout:
            self.wait_for_clickability(timeout)

        logger.info("%r clicking ...", self)
        self._el.click()


class Checkbox(PageElement):
    """ Checkbox descriptor"""
    def __get__(self, instance, owner):
        return CheckboxWrapper(self.find(instance.webdriver), self._locator)

    def __set__(self, instance, value):
        if value is None:
            return

        element = self.__get__(instance, instance.__class__)
        if value:
            element.check()
        else:
            element.uncheck()
