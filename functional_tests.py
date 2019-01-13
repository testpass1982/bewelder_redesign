from selenium import webdriver
import unittest

# Мы проверяем этим тестом функциональность приложения
# с помощью selenium
# руководство по установке и запуску selenium по ссылке ниже:
# https://selenium-python.com/install-geckodriver

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_bewelder_main_page(self):
        # Запустив dev-server командой python manage.py runserver
        # в другой консоли мы запускаем на исполнение функциональное
        # тестирование командой python functional_tests.py
        # прежде всего мы проверяем загузку заголовка главной страницы "Bewelder"

        self.browser.get('http://localhost:8000')
        self.assertIn('Bewelder learning project', self.browser.title)
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')

