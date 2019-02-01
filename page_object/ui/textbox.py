# -*- coding: utf-8 -*-

import logging

from page_object import PageElement, PageElementWrapper

__all__ = ['Textbox', 'TextboxWrapper']


class TextboxWrapper(PageElementWrapper):
    """ Wrapper for <input type="text">"""

    def enter_text(self, text, timeout=0, clear=True):
        if timeout:
            self.wait_for_clickability(timeout)

        if clear:
            logging.info("%s cleaning ...", self)
            self._el.clear()

        logging.info("%s entering text ...", self)
        self._el.send_keys(text)


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
