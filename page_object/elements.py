# -*- coding: -utf-8 -*-

from page_object import PageElement


class BaseElement(PageElement):
    @property
    def is_enabled(self):
        return self._element.is_enabled()

    @property
    def is_visible(self):
        return self._element.is_displayed()

    @property
    def text(self):
        return self._element.text

    @property
    def value(self):
        return self._element.get_attribute('value')


class CheckableElement(BaseElement):
    @property
    def checked(self):
        return self._element.is_selected()

    @checked.setter
    def checked(self, checked):
        if checked is not None:
            if checked and not self.checked:
                self._element.click()
            if not checked and self.checked:
                self._element.click()


class ClickableElement(BaseElement):
    def click(self):
        self._element.click()


class Checkbox(CheckableElement): pass


class RadioButton(CheckableElement): pass


class Button(ClickableElement): pass


class Link(ClickableElement): pass


class Select(BaseElement):
    @property
    def options(self):
        return self._element.find_elements_by_tag_name('option')

    def select(self, value):
        value = str(value)
        if len(value) > 0:
            for option in self.options:
                if value in option.text:
                    option.click()


class Textbox(BaseElement):
    def __set__(self, instance, value):
        value = str(value)
        if len(value) > 0:
            if self._element is None:
                self.__get__(instance, instance.__class__)
            self._element.send_keys(value)

    def clear(self):
        self._element.clear()
