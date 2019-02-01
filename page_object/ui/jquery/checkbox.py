# -*- coding: utf-8 -*-

import logging

from page_object import PageElement, PageElementWrapper

__all__ = ['Checkbox', 'CheckboxWrapper']


class CheckboxWrapper(PageElementWrapper):
    """ Wrapper for <input type="checkbox">"""

    @property
    def checked(self):
        return self._el.parent.execute_script(
            'return $("{}").prop("checked");'.format(self._locator[1]))

    def check(self):
        logging.info("%s checking ...", self)
        self._el.parent.execute_script(
            'return $("{}").prop("checked", true).change();'.format(
                self._locator[1]))

    def uncheck(self):
        logging.info("%s unchecking ...", self)
        self._el.parent.execute_script(
            'return $("{}").prop("checked", false).change();'.format(
                self._locator[1]))


class Checkbox(PageElement):
    """ Checkbox descriptor"""

    def __get__(self, instance, owner):
        el = CheckboxWrapper(self.find(instance.webdriver), self._locator)
        el.move_to_self()
        return el

    def __set__(self, instance, value):
        if value is None:
            return

        element = self.__get__(instance, instance.__class__)
        if value:
            element.check()
        else:
            element.uncheck()
