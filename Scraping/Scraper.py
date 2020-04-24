from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import requests
import os
from PIL import Image
from urllib.request import urlopen

class ScraperGoogle():

	def __init__(self):
		self.driver=Chrome()
		self.tmp()
	def tmp(self):
		self.driver.get('https://google.com')
		assert("Google" in self.driver.title)
		search = self.driver.find_element_by_name("q")
		search.send_keys("dogs",Keys.RETURN)
		images = self.driver.find_element_by_css_selector("a.q")
		images.click()
		#here we are in google images
		first_img = self.driver.find_element_by_xpath("//img[@data-deferred='1']")
		first_img.click()

		self.load_picture()

	def load_picture(self):
		srcs = set()
		image = self.driver.find_element_by_xpath("//img[@jsaction='load:XAeZkd;']")
		#this image must be dawloanded end go to the next
		image_src=image.get_attribute("src")
		srcs.add(image_src)






X=ScraperGoogle()

