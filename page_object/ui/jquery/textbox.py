# -*- coding: utf-8 -*-

import logging

from page_object import PageElement, PageElementWrapper

__all__ = ['Textbox', 'TextboxWrapper']


class TextboxWrapper(PageElementWrapper):
    """ JQuery wrapper for <input type="text">"""
    @property
    def value(self):
        return self._el.parent.execute_script(
            'return $("{}").val();'.format(self._locator[1]))

    def enter_text(self, text):
        logging.info("%s entering text ...", self)
        self._el.parent.execute_script(
            """
            $("{0}").val("{1}").change();
            """.format(self._locator[1], text))


class Textbox(PageElement):
    """ Textbox descriptor"""

    def __get__(self, instance, owner):
        return TextboxWrapper(self.find(instance.webdriver), self._locator)

    def __set__(self, instance, value):
        if value is None:
            return

        value = str(value).strip()
        if not value:
            return

        self.__get__(instance, instance.__class__).enter_text(value)
