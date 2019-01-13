from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import configparser
import ast

class JokerFinder:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('conf.ini')
        #self.driver = webdriver.Chrome('chromedriver\\chromedriver.exe')

        self.places= ast.literal_eval(self.config['SELECTED_LOCATIONS']['LOCATIONS'])
        self.url= 'https://www.yemeksepeti.com'
        self.username = self.config['USER']['USERNAME']
        self.password = self.config['USER']['PASSWORD']
        self.time_to_wait = int(self.config['DEFAULT']['TIME_TO_WAIT'])
        self.current_page= 0
        self._check_selected_locations()
        self._check_user_cred()

    def _check_selected_locations(self):

        self.selected_location = self.config['SELECTED_LOCATIONS']['SELECTED_LOCATION']
        if self.selected_location is '':
            user_input = input('Arama yapılacak bölgeyi yazınız: For ex: besiktas')
            locations = [i for i in self.places if user_input in i]
            self._update_config('SELECTED_LOCATIONS','SELECTED_LOCATION',str(locations))

    def _check_user_cred(self):
        if self.username is '':
            user_input = input('Username: ')
            self._update_config('USER','USERNAME',user_input)

        if self.password is '':
            user_input = input('Password: ')
            self._update_config('USER', 'PASSWORD', user_input)

    def _update_config(self,system,variable,value):
        self.config.set(system,variable,value)
        with open("conf.ini", "w+") as configfile:
            self.config.write(configfile)

    def login(self):
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/a[28]').click()
        except Exception as e:
            pass
        username_field = self.driver.find_element_by_id('UserName')
        username_field.click()
        username_field.send_keys(self.username)
        password_field = self.driver.find_element_by_id('password')
        password_field.click()
        password_field.send_keys(self.password)
        self.driver.find_element_by_id('ys-fastlogin-button').click()

    def change_page(self):
        self.current_page = ((self.current_page +1) % len(self.places))
        self.driver.get("https://www.yemeksepeti.com" + self.places[self.current_page])

    def search(self):
        pass

    def _run(self):
        pass
        #self.driver.get("https://www.yemeksepeti.com" + self.places[self.current_page])
        #self.login()
        #while True:
            #time.sleep(self.time_to_wait)
            #self.change_page()
JokerFinder()._run()
"""     
try:
    driver = webdriver.Chrome('chromedriver\\chromedriver.exe')
    driver.get("https://www.yemeksepeti.com/")
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/a[28]').click()
    username_field=driver.find_element_by_id('UserName')
    username_field.click()
    username_field.send_keys('mgokberkoguz1@gmail.com')
    password_field=driver.find_element_by_id('password')
    password_field.click()
    password_field.send_keys('159753')
    driver.find_element_by_id('ys-fastlogin-button').click()
    time.sleep(5)
except:
    driver.close()

try:
    element = driver.find_element_by_id('/html/body/header/div[2]/div/div/div[2]/span')
    #driver.execute_script("arguments[0].setAttribute('select2-selection__rendered','vote-link up voted')", element)
except Exception as e:
    print(e)
    #driver.close()
"""

