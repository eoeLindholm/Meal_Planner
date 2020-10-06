#Qt Imports
from PySide2 import QtWidgets
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (QApplication, QLabel, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QHBoxLayout, QSpinBox)
#Other Imports
from selenium import webdriver
import time

from selenium.common.exceptions import ElementClickInterceptedException


class CityGrossScraper:
    PATH = "C:/Program Files (x86)/chromedriver.exe"

    def run(self, username, password):
        self.driver = webdriver.Chrome(self.PATH)
        self.login(username, password)
        self.goto_offers()
        self.expand_offers()
        self.offers = self.get_offers()
        self.driver.quit()

    # Log in
    def login(self, username, password):
        self.driver.get("https://www.citygross.se/login")
        email = username
        username_entry = self.driver.find_element_by_id("username")
        username_entry.send_keys(email)
        password_entry = self.driver.find_element_by_id("password")
        password_entry.send_keys(password)
        login_btn = self.driver.find_element_by_xpath(
            "//button[@type='submit' and @class='c-cmdbtn undefined prio fullwidth']")
        login_btn.click()

        time.sleep(2)

    # Go to "Veckans Erbjudanden"
    def goto_offers(self):
        offers_btn = self.driver.find_element_by_link_text("Se fler erbjudanden")
        try:
            offers_btn.click()
        except ElementClickInterceptedException:
            cookie_btn = self.driver.find_element_by_css_selector("#citygross > div.c-cookie-container__desktop > div > div > button")
            cookie_btn.click()
            self.goto_offers()

        time.sleep(2)

    # Expand to all offers
    def expand_offers(self):
        total_offers = self.driver.find_element_by_class_name("c-loadmore__status")
        tot_offers = int(total_offers.text[12:15])

        for i in range(tot_offers // 20):
            offers_btn = self.driver.find_element_by_class_name("c-loadmore__button")
            offers_btn.click()
            time.sleep(2)

    # Get offers and returns them as list of strings
    def get_offers(self):
        main_items = self.driver.find_elements_by_tag_name("h2")
        filler_items = self.driver.find_elements_by_tag_name("h3")
        integer_price = self.driver.find_elements_by_css_selector("span.integer")
        fractions_price = self.driver.find_elements_by_class_name("fractions")
        unit_price = self.driver.find_elements_by_class_name("unit")

        insert_index = []

        for i in range(len(main_items)):
            main_items[i] = main_items[i].text
        for i in range(len(filler_items)):
            filler_items[i] = filler_items[i].text
        for i in range(len(integer_price)):
            if ":-" in integer_price[i].text:
                insert_index.append(i)
                if not ord(integer_price[i].text[2]) == 10 and not ord(integer_price[i].text[1]) == 10:
                    integer_price[i] = integer_price[i].text[0:3]
                elif not ord(integer_price[i].text[1]) == 10 and ord(integer_price[i].text[2]) == 10:
                    integer_price[i] = integer_price[i].text[0:2]
                else:
                    integer_price[i] = integer_price[i].text[0:2]

            else:
                integer_price[i] = integer_price[i].text
        for i in range(len(fractions_price)):
            fractions_price[i] = fractions_price[i].text
        for i in range(len(unit_price)):
            unit_price[i] = unit_price[i].text[1:3]

        for i in range(len(insert_index)):
            fractions_price.insert(insert_index[i], "00")
            unit_price.insert(insert_index[i], "st")

        unit_price.remove("")
        unit_price.remove("")

        offers_list = []
        for i in range(len(main_items)):
            offer = [main_items[i] + " " + filler_items[i], integer_price[i] + "." + fractions_price[i], unit_price[i]]
            offers_list.append(offer)

        return offers_list


class ScraperWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0

        #Temp Data
        self._data = None

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Item", "Price", "Unit"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.email = QLineEdit()
        self.email_layout = QVBoxLayout()
        self.email_layout.addWidget(QLabel("Email:"))
        self.email_layout.addWidget(self.email)

        self.password = QLineEdit()
        self.password_layout = QVBoxLayout()
        self.password_layout.addWidget(QLabel("Password:"))
        self.password_layout.addWidget(self.password)

        self.input_layout = QHBoxLayout()
        self.input_layout.addLayout(self.email_layout)
        self.input_layout.addLayout(self.password_layout)

        self.btn_get = QPushButton("Get Offers")
        self.btn_clear = QPushButton("Clear")
        self.btn_quit = QPushButton("Quit")

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.input_layout)
        self.layout.addWidget(self.btn_get)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btn_clear)
        self.layout.addWidget(self.btn_quit)
        self.setLayout(self.layout)

        self.btn_get.clicked.connect(self.get_offers_cmd)
        self.btn_clear.clicked.connect(self.clear_table)
        self.btn_quit.clicked.connect(self.quit_application)

    @Slot()
    def get_offers_cmd(self):
        username = self.email.text()
        password = self.password.text()
        self.email.setText("")
        self.password.setText("")
        scraper = CityGrossScraper()
        scraper.run(username, password)
        self.fill_table(scraper.offers)

    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0

    @Slot()
    def quit_application(self):
        QApplication.quit()

    def fill_table(self, data=None):
        data = self._data if not data else data
        for item in data:
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, QTableWidgetItem(item[0]))
            self.table.setItem(self.items, 1, QTableWidgetItem(item[1]))
            self.table.setItem(self.items, 2, QTableWidgetItem(item[2]))
            self.items += 1
