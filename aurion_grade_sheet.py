""""
Class to get grades from WebAurion using Selenium
"""

import keyring
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from webdriver_manager.microsoft import EdgeChromiumDriverManager


class AurionAccess:
    """
    get grades from WebAurion using Selenium
    """
    def __init__(self):
        self._driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        self._driver.get("https://webaurion.ensea.fr/faces/Login.xhtml")
        self._username = input("Entrez votre nom d' utilisateur WebAurion : \n")
        self.grades = None

    @property
    def _password(self):
        return keyring.get_password("webaurion", self._username)

    def login(self):
        username_input = self._driver.find_element_by_xpath('//*[@id="username"]')
        username_input.send_keys(self._username)
        password_input = self._driver.find_element_by_xpath('//*[@id="password"]')
        password_input.send_keys(self._password)
        connexion_button = self._driver.find_element_by_xpath('//*[@id="formulaireSpring"]/div[4]')
        connexion_button.click()

    def get_marks_from_aurion(self):

        scolarite_entry = self._driver.find_element_by_xpath("(//span[@class='ui-menuitem-text'])[3]")
        scolarite_entry.click()
        mes_notes_entry = WebDriverWait(self._driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="form:sidebar"]/div/div[2]/ul/li[3]/ul/li/a'))
        )
        mes_notes_entry.click()

        self.grades = pd.read_html(self._driver.page_source)[0]
        new_names = []
        for column in self.grades:
            bad_string = column.split("Filter by")[0]
            self.grades[column] = self.grades[column].str.replace(bad_string, '')

            new_names.append(column.split("Filter by")[0])
        self.grades.columns = new_names
        self.grades.to_csv("OOP-Test.csv", encoding='utf-16')
        self._driver.close()

    def get_marks(self):
        return self.grades


if __name__ == "__main__":
    Aurion = AurionAccess()
    Aurion.login()
    Aurion.get_marks_from_aurion()
