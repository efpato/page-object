# -*- coding: -utf-8 -*-

import logging

from page_object import PageElement, PageElementError

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class CheckableElement(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            element = self.__get__(instance, instance.__class__)
            if (value and not element.is_selected()) or \
                    (not value and element.is_selected()):
                logging.info("Click checkable element by %s: <%s>",
                             *self._locator)
                element.click()
                return 1


class Clickable(PageElement):
    def __get__(self, instance, owner):
        element = PageElement.__get__(self, instance, owner)
        WebDriverWait(instance.webdriver, PageElement.TIMEOUT).until(
            expected_conditions.element_to_be_clickable(self._locator),
            "Not found element by %s: <%s> or element is not clickable" %
            self._locator)
        return element


class Checkbox(CheckableElement):
    pass


class Radio(CheckableElement):
    pass


class Button(Clickable):
    pass


class Link(Clickable):
    pass


class Select(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            value = str(value).strip()
            element = self.__get__(instance, instance.__class__)
            if len(value) > 0:
                for option in element.find_elements_by_xpath("./option"):
                    if option.text.strip() == value:
                        logging.info(
                            "Select option '%s' for element <%s>: <%s>",
                            value, self._locator[0], self._locator[1])
                        option.click()
                        return 1
                raise PageElementError(
                    "Select<%s> has no option with text '%s'" %
                    (self._locator[1], value))


class Textbox(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            element = self.__get__(instance, instance.__class__)
            value = str(value)
            if len(value) > 0:
                logging.info("Type text '%s' into element <%s>: <%s>",
                             value, self._locator[0], self._locator[1])
                element.clear()
                element.send_keys(value)
                return 1
