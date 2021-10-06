import urllib.parse

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.support.select import Select


class CustomWebDriver(Chrome):
    def open(self, url):
        if urllib.parse.unquote(self.current_url) != url:
            self.get(url)


class CustomSelect(Select):
    def get_option_value_by_text_contains(self, text):
        for op in self.options:
            if text.lower() in op.text.lower():
                return op.get_attribute("value")


class TurkeyPostalCodes:
    def __init__(self):
        extensions = []
        options = chrome_options()
        options.headless = True
        for extension in extensions:
            options.add_extension(extension)
        self.driver = CustomWebDriver(executable_path="driver/chromedriver.exe", options=options)
        self.driver.open("https://postakodu.ptt.gov.tr/")

    def get_postal_code(self, city_name, district_name, township_name):
        self.select_city(city_name)
        self.select_district(district_name)
        self.select_township(township_name)
        return self.get_postal_code_text()

    def select_city(self, city_name):
        city_select_xpath = """//*[@id="MainContent_DropDownList1"]"""
        city_select = Select(self.driver.find_element_by_xpath(city_select_xpath))
        city_select.select_by_visible_text(city_name)

    def select_district(self, district_name):
        district_select_xpath = """//*[@id="MainContent_DropDownList2"]"""
        district_select = Select(self.driver.find_element_by_xpath(district_select_xpath))
        district_select.select_by_visible_text(district_name)

    def select_township(self, township_name):
        township_select_xpath = """//*[@id="MainContent_DropDownList3"]"""
        township_select = CustomSelect(self.driver.find_element_by_xpath(township_select_xpath))
        option_value = township_select.get_option_value_by_text_contains(township_name)
        township_select.select_by_value(option_value)

    def get_postal_code_text(self):
        postal_code_xpath = """//*[@id="MainContent_Label1"]"""
        postal_code_text = self.driver.find_element_by_xpath(postal_code_xpath).text
        return postal_code_text


if __name__ == '__main__':
    tpc = TurkeyPostalCodes()
    print(tpc.get_postal_code("KONYA", "SELÇUKLU", "MEHMET AKİF"))
    print(tpc.get_postal_code("ARTVİN", "MERKEZ", "AKTAŞ"))
    print(tpc.get_postal_code("AYDIN", "KÖŞK", "CUMADERE"))
