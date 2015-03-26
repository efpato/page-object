# -*- coding: -utf-8 -*-

from page_object import PageElement


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
        value = str(value)
        if len(value) > 0:
            element = self.__get__(instance, instance.__class__)
            for option in element.find_elements_by_tag_name('option'):
                if value in option.text:
                    option.click()


class Textbox(PageElement):
    def __set__(self, instance, value):
        value = str(value)
        if len(value) > 0:
            self.__get__(instance, instance.__class__).send_keys(value)
