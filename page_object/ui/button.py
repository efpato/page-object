# -*- coding: utf-8 -*-

import logging

from page_object import PageElement, PageElementWrapper

__all__ = ['Button', 'ButtonWrapper', 'Link']

logger = logging.getLogger(__name__)


class ButtonWrapper(PageElementWrapper):
    """ Wrapper for <input type="button">"""

    def click(self, timeout=0):
        if timeout:
            self.wait_for_clickability(timeout)

        logger.info("%r clicking ...", self)
        self._el.click()


class Button(PageElement):
    """ Button descriptor"""

    def __get__(self, instance, owner):
        el = ButtonWrapper(self.find(instance.webdriver), self._locator)
        el.move_to_self()
        return el


Link = Button
