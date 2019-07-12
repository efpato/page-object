# -*- coding: utf-8 -*-

import logging

from page_object import PageElement, PageElementWrapper

__all__ = ['Radio', 'RadioWrapper']

logger = logging.getLogger(__name__)


class RadioWrapper(PageElementWrapper):
    """ Wrapper for <input type="radio">"""

    @property
    def checked(self):
        logger.info("%r is checked ...", self)
        return self._el.is_selected()

    def click(self, timeout=0):
        if timeout:
            self.wait_for_clickability(timeout)

        logger.info("%r clicking ...", self)
        self._el.click()


class Radio(PageElement):
    """ Radio descriptor"""

    def __get__(self, instance, owner):
        el = RadioWrapper(self.find(instance.webdriver), self._locator)
        el.move_to_self()
        return el
