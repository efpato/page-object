# -*- coding: utf-8 -*-

import time

from page_object import PageElement, PageElementInterace


__all__ = ['Input', 'AutoInput']


class InputInterface(PageElementInterace):
    @property
    def value(self):
        return self._el.parent.execute_script(
            'return $("{}").val();'.format(self._locator[1]))


class Input(PageElement):
    def __get__(self, instance, owner):
        element = super(Input, self).__get__(instance, owner)
        return InputInterface(element, self._locator)

    def __set__(self, instance, value):
        if value is None:
            return

        value = str(value).strip()
        if not value:
            return

        self.__get__(instance, instance.__class__)
        instance.webdriver.execute_script(
            """
            $("{0}").val("{1}").change();
            """.format(self._locator[1], value))


class AutoInput(Input):
    def __set__(self, instance, value):
        if value is None:
            return

        value = str(value).strip()
        if not value:
            return

        self.__get__(instance, instance.__class__)
        instance.webdriver.execute_script(
            """
            $("{0}").val("{1}").change();
            setTimeout(function () {{
                $("{0} ~ ul li").first().click();
            }}, 3000);
            """.format(self._locator[1], value))
        time.sleep(3.5)
