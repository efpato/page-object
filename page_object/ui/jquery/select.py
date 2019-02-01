# -*- coding: utf-8 -*-

import logging

from page_object import PageElement, PageElementWrapper

__all__ = ['Select', 'SelectWrapper']


class SelectWrapper(PageElementWrapper):
    @property
    def options(self):
        return self._el.find_elements_by_tag_name('option')

    @property
    def text(self):
        return self._el.parent.execute_script(
            """
            return $("{} :selected").text();
            """.format(self._locator[1]))

    @property
    def value(self):
        return self._el.parent.execute_script(
            """
            return $("{}").val();
            """.format(self._locator[1]))

    def select_by_text(self, text):
        logging.info('%s selecting by text "%s" ...', self, text)
        self._el.parent.execute_script(
            """
            return $("{0} option").filter(function () {{
                return $.trim($(this).text()) == '{1}';
            }}).attr('selected', 'selected').change();
            """.format(self._locator[1], text))

    def select_by_value(self, value):
        logging.info('%s selecting by value "%s" ...', self, value)
        self._el.parent.execute_script(
            """
            return $("{0} [value='{1}']")
                .attr('selected', 'selected')
                .change();
            """.format(self._locator[1], value))


class Select(PageElement):
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
