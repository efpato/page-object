# -*- coding: utf-8 -*-

import logging

from page_object import PageElement, PageElementWrapper

__all__ = ['Textbox', 'TextboxWrapper']

logger = logging.getLogger(__name__)


class TextboxWrapper(PageElementWrapper):
    """ Wrapper for <input type="text">"""

    def enter_text(self, text, timeout=0, clear=True):
        if timeout:
            self.wait_for_clickability(timeout)

        if clear:
            logger.info("%r cleaning ...", self)
            self.clear()

        logger.info("%r entering text ...", self)
        self.send_keys(text)


class Textbox(PageElement):
    """ Textbox descriptor"""

    def __get__(self, instance, owner):
        el = TextboxWrapper(self.find(instance.webdriver), self._locator)
        el.move_to_self()
        return el

    def __set__(self, instance, value):
        if value is None:
            return

        value = str(value).strip()
        if not value:
            return

        self.__get__(instance, instance.__class__).enter_text(value)
