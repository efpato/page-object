Page Objects for Python
=======================

Selenium Page Objects for Python.

#Installation
```bash
$ python setup.py install
```

#Quick Example

```python
from selenium.webdriver import Firefox

from page_object import PageObject
from page_object.elements import Link, Button, Textbox
 

class HomePage(PageObject):
    news = Link(link_text="news")


class LoginPage(PageObject):
    username = Textbox(name="username")
    password = Textbox(name="password")
    login = Button(xpath="//input[@value='Log in']")

    def logIn(self, username, password):
        self.username = username
        self.password = password
        self.login.click()
        return HomePage(self.webdriver)


driver = Firefox()
driver.maximize_window()
 
page = LoginPage(driver, 'http://localhost:8000')
page.get('/login')
page = page.logIn('user', 'passwd')
assert "My site" in page.title, 'Fail login'

driver.quit()
```
