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

    def enter_text(self, value):
        logging.info("%s entering text `%s` ...", self, value)
        self._el.parent.execute_script(
            """
            $("{0}").val("{1}").change();
            """.format(self._locator[1], value))

    def enter_number(self, value):
        logging.info("%s entering number `%s` ...", self, value)
        self._el.parent.execute_script(
            """
            $("{0}").val({1}).change();
            """.format(self._locator[1], value))


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
