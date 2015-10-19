# -*- coding: -utf-8 -*-

from page_object import PageElement, PageElementError


class CheckableElement(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            element = self.__get__(instance, instance.__class__)
            if (value and not element.is_selected()) or (not value and element.is_selected()):
                element.click()


class Checkbox(CheckableElement):
    pass


class Radio(CheckableElement):
    pass


class Button(PageElement):
    pass


class Link(PageElement):
    pass


class Select(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            value = str(value).strip()
            element = self.__get__(instance, instance.__class__)
            if len(value) > 0:
                for option in element.find_elements_by_xpath("./option"):
                    if option.text.strip() == value:
                        option.click()
                        return 1
                raise PageElementError("""Select<"%s"> has no option with text "%s" """ % (self._locator[1], value))


class Textbox(PageElement):
    def __set__(self, instance, value):
        if value is not None:
            element = self.__get__(instance, instance.__class__)
            value = str(value)
            if len(value) > 0:
                element.clear()
                element.send_keys(value)
