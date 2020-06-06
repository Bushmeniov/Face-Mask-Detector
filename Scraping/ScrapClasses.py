from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

import requests
import os
from PIL import Image
import time
import io
import hashlib
import numpy as np

'''from tensorflow.keras.models import load_model
model = load_model('/home/vladislav/PycharmProjects/tftest/Models/MobileNET.h5')
model.load_weights('/home/vladislav/PycharmProjects/tftest/Models/MobileNET_weights.h5')'''

class ScraperGoogle():

	def __init__(self,what_to_scrap,max_fetches,folder_path):
		'''
		:param what_to_scrap: type photos(cat,human,car)
		:param max_fetches: max N photos to scrap
		:param folder_path: path for saving photos
		'''

		self.driver=Chrome() # driver object to manage browser
		# Google URL, where actions will take place
		self.URL = f"https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={what_to_scrap}&oq=" \
				   f"{what_to_scrap}&gs_l=img"

		self.folder_path=folder_path
		self.what_to_scrap=what_to_scrap
		self.max_fetches=max_fetches


		self.URLSset=set() # all URLs of scraping Images

	def get_URLS_len(self):
		"""return len of scraping Images"""
		return len(self.URLSset)

	def run(self):
		"""RUN Scraping"""

		self.steal_photos_url()

	def steal_photos_url(self):

		self.driver.get(self.URL)

		start=0

		while self.get_URLS_len()<self.max_fetches:

			urls_tmp = set()

			#scrolling page
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(3) # for correct respond
			#all mini_images on which are visible in css
			mini_images = self.driver.find_elements_by_css_selector("img.Q4LuWd")
			end = len(mini_images)

			for image in mini_images[start:end] :

				try :
					image.click() # click to activate image and fetch the src with http
					time.sleep(1)

				except Exception:
					continue

				actual_images=self.driver.find_elements_by_css_selector('img.n3VNCb')

				for actual_image in actual_images:
					#filter
					if actual_image.get_attribute("src") and ('http' in actual_image.get_attribute('src')):
						urls_tmp.add(actual_image.get_attribute("src"))

			else:

				# if we see button : "Dowload more"
				load_more_button = self.driver.find_element_by_css_selector('.mye4qd')

				if load_more_button  :
					self.driver.execute_script("document.querySelector('.mye4qd').click();")
					time.sleep(3)

			start = end
			#new URLs

			self.dowload_batch_images(urls_tmp)


	def dowload_batch_images(self,urls_tmp):
		difference = urls_tmp - self.URLSset

		for src in difference:
			self.dawload_image(src)

		self.URLSset = self.URLSset.union(difference)


	def dawload_image(self,URL):

		try :
			image_content = requests.get(URL).content # fetching image bytes

		except Exception as e :
			print(f"Image content error - {e}")

		try :
			image_file = io.BytesIO(image_content)
			image = Image.open(image_file).convert("RGB")
			# hash our image
			file_path=os.path.join(self.folder_path,hashlib.sha1(image_content).hexdigest()[:12] + '.jpg')

			with open(f"{file_path}","wb") as f :
				image.save(f,"JPEG",quality=85)


		except Exception as e :
			print(f"Error - couldn't save - {e}")

'''	def dawload_image(self,URL):
		"""WITH FILTERING"""
		try:
			image_content = requests.get(URL).content  # fetching image bytes

		except Exception as e:
			print(f"Image content error - {e}")

		try:
			image_file = io.BytesIO(image_content)
			image = Image.open(image_file).convert("RGB")

			tmp = int(model.predict(np.asarray(image.resize((224, 224))).reshape(1, 224, 224, 3))[0][0])

			if not tmp:
				file_path = os.path.join(self.folder_path,
											 hashlib.sha1(image_content).hexdigest()[:12] + '.jpg')

				with open(f"{file_path}", "wb") as f:
					image.save(f, "JPEG", quality=85)


		except Exception as e:
			print(f"Error - couldn't save - {e}")'''


class ScraperPixabay(ScraperGoogle):

	def __init__(self,what_to_scrap,max_fetches,folder_path):
		super().__init__(what_to_scrap,max_fetches,folder_path)
		self.URL = f"https://pixabay.com/ru/images/search/{what_to_scrap}"

	def steal_photos_url(self):

		pagi = 1
		URL_additional='/?pagi='
		while  self.get_URLS_len() < self.max_fetches:

			self.driver.get(self.URL+URL_additional+str(pagi))
			time.sleep(3)
			urls_tmp = self.scrapImagesOnPage()
			pagi+=1

			self.dowload_batch_images(urls_tmp)

	def scrapImagesOnPage(self):
		pos = 800
		_set=set()
		for i in range(15):
			images = self.driver.find_elements_by_css_selector('img')
			for image in images:
				if image.get_attribute("src") and ('http' in image.get_attribute('src')) \
						and (".jpg" in image.get_attribute("src")):
					_set.add(image.get_attribute("src"))
			self.driver.execute_script(f"window.scrollTo(0, {pos});")
			pos+=800
			time.sleep(1)


		return _set


class UnsplashScrapper(ScraperGoogle):

	def __init__(self,what_to_scrap,max_fetches,folder_path):
		super().__init__(what_to_scrap,max_fetches,folder_path)
		self.URL = f"https://unsplash.com/s/photos/{what_to_scrap}"

	def steal_photos_url(self):

		self.driver.get(self.URL)
		pos = 800
		while self.get_URLS_len() < self.max_fetches:
			urls_tmp = set()  # set of URLs

			images = self.driver.find_elements_by_css_selector('img')
			for image in images:
				if image.get_attribute("src"):
					src = image.get_attribute("src")
					if  ('http' in src) and ("profile" not in src) and ('Images.unsplash.com' in src)  \
								and ("avatars" not in src):
						urls_tmp.add(image.get_attribute("src"))
			self.driver.execute_script(f"window.scrollTo(0, {pos});")
			time.sleep(5)
			pos+=800

			self.dowload_batch_images(urls_tmp)


class PexelsScrapper(ScraperGoogle):

	def __init__(self,what_to_scrap,max_fetches,folder_path):
		super().__init__(what_to_scrap,max_fetches,folder_path)
		self.URL = f"https://www.pexels.com/ru-ru/search/{what_to_scrap}"

	def steal_photos_url(self):

		self.driver.get(self.URL)
		pos = 800
		start=0
		while self.get_URLS_len() < self.max_fetches:

			urls_tmp = set()  # set of URLs

			images = self.driver.find_elements_by_css_selector('img')
			end = len(images)

			for image in images[start:end]:
				if image.get_attribute("src"):
					src=image.get_attribute("src")
					if ('https://images.pexels.com/' in src) and (".jpeg" in src) and ("profile" not in src) \
								and	("users" not in src) and ("avatars" not in src):

						urls_tmp.add(image.get_attribute("src"))
			self.driver.execute_script(f"window.scrollTo(0, {pos});")
			time.sleep(5)
			pos += 800

			start=end
			self.dowload_batch_images(urls_tmp)

class InstagramScraper(ScraperGoogle):
	def __init__(self,what_to_scrap,max_fetches,folder_path):
		super().__init__(what_to_scrap,max_fetches,folder_path)
		self.URL = f"https://www.instagram.com/explore/tags/{what_to_scrap}/"

	def steal_photos_url(self):

		self.driver.get(self.URL)
		time.sleep(240)

		pos = 800
		start = 0
		while self.get_URLS_len() < self.max_fetches:

			urls_tmp = set()  # set of URLs

			images = self.driver.find_elements_by_css_selector('img')
			end = len(images)


			for image in images[start:end]:
				if image.get_attribute("src"):
					src = image.get_attribute("src")
					if ('https://instagram.fiev12-1.fna.fbcdn.net/' in src) and (".jpg" in src) :
						urls_tmp.add(image.get_attribute("src"))
			self.driver.execute_script(f"window.scrollTo(0, {pos});")
			time.sleep(6)
			pos += 800

			start = end
			self.dowload_batch_images(urls_tmp)


scrapGoogle2=ScraperGoogle(what_to_scrap="вещи",max_fetches=400,
						  folder_path="/home/vladislav/PycharmProjects/tftest/third class/games")

scrapPixabay=ScraperPixabay(what_to_scrap="room",max_fetches=800,
						  folder_path="/home/vladislav/PycharmProjects/tftest/without_people_images")

scrapUnsplash=UnsplashScrapper(what_to_scrap="animals",max_fetches=800,
						folder_path="/home/vladislav/PycharmProjects/tftest/without_people_images")

scrapPexels=PexelsScrapper(what_to_scrap="street",max_fetches=800,
						   folder_path="/home/vladislav/PycharmProjects/tftest/without_people_images")

InstagramScraper1=InstagramScraper(what_to_scrap="dailyselfie",max_fetches=10000,
						   folder_path='/home/vladislav/PycharmProjects/tftest/insta_without')




if "__main__" == "__main__":

	from multiprocessing import Process

	def run(scraperObj):
		#activate scraping
		scraperObj.run()

	def start_scraping():

		processes = []

		for scraper in (scrapGoogle2,scrapPixabay,scrapUnsplash,scrapPexels,InstagramScraper1):
			process=Process(target=run,args=(scraper,))
			processes.append(process)
			process.start()
		for process in processes:
			
			process.join()

	start_scraping()