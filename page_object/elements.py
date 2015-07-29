# -*- coding: -utf-8 -*-

from page_object import PageElement

from selenium.webdriver.support.wait import WebDriverWait


class CheckableElement(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            element = self.__get__(instance, instance.__class__)
            if (value and not element.is_selected()) or (not value and element.is_selected()):
                element.click()


class Checkbox(CheckableElement): pass


class Radio(CheckableElement): pass


class Button(PageElement): pass


class Link(PageElement): pass


class Select(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            value = str(value)
            if len(value) > 0:
                WebDriverWait(instance.webdriver, self.TIMEOUT).until(
                    lambda d: self.find(d).find_element_by_xpath("./option[text()='%s']" % value),
                    "Didn\'t find option by text='%s'." % value).click()


class Textbox(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            value = str(value)
            if len(value) > 0:
                self.__get__(instance, instance.__class__).send_keys(value)
