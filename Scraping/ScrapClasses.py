from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

import requests
import os
from PIL import Image
import time
import io
import hashlib

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

	def run(self):
		"""RUN Scraping"""

		_URLs=self.steal_photos_url()

		'''for url in _URLs:
			self.dawload_image(url)'''

	def steal_photos_url(self):

		urls_tmp = set()  # set of URLs

		self.driver.get(self.URL)

		start=0

		while len(urls_tmp)<self.max_fetches:

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

		return urls_tmp

	def dawload_image(self,URL):

		try :
			image_content = requests.get(URL).content # fetching image bytes

		except Exception as e :
			print(f"Image content error - {e}")

		try :
			image_file = io.BytesIO(image_content)
			image = Image.open(image_file).convert("RGB")
			# hash our image
			file_path=os.path.join(self.folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')

			with open(f"{file_path}","wb") as f :
				image.save(f,"JPEG",quality=85)


		except Exception as e :
			print(f"Error - couldn't save - {e}")



class ScraperPixabay(ScraperGoogle):

	def __init__(self,what_to_scrap,max_fetches,folder_path):
		super().__init__(what_to_scrap,max_fetches,folder_path)
		self.URL = f"https://pixabay.com/ru/images/search/{what_to_scrap}"

	def steal_photos_url(self):
		urls_tmp = set()  # set of URLs
		pagi = 1
		URL_additional='/?pagi='
		while  len(urls_tmp) < self.max_fetches:
			self.driver.get(self.URL+URL_additional+str(pagi))
			time.sleep(3)
			data = self.scrapImagesOnPage()
			urls_tmp=urls_tmp.union(data)
			pagi+=1

		return urls_tmp

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
		urls_tmp = set()  # set of URLs
		self.driver.get(self.URL)
		pos = 800
		while len(urls_tmp) < self.max_fetches:

			images = self.driver.find_elements_by_css_selector('img')
			for image in images:
				if image.get_attribute("src") and ('http' in image.get_attribute('src'))\
						and ("profile" not in image.get_attribute("src")) and \
						('images.unsplash.com' in image.get_attribute("src")) and \
						("avatars" not in image.get_attribute("src")):
					urls_tmp.add(image.get_attribute("src"))
			self.driver.execute_script(f"window.scrollTo(0, {pos});")
			time.sleep(1.5)
			pos+=800

		return urls_tmp



class PexelsScrapper(ScraperGoogle):

	def __init__(self,what_to_scrap,max_fetches,folder_path):
		super().__init__(what_to_scrap,max_fetches,folder_path)
		self.URL = f"https://www.pexels.com/ru-ru/search/{what_to_scrap}"

	def steal_photos_url(self):
		urls_tmp = set()  # set of URLs
		self.driver.get(self.URL)
		pos = 800
		while len(urls_tmp) < self.max_fetches:

			images = self.driver.find_elements_by_css_selector('img')
			for image in images:
				if image.get_attribute("src") and ('https://images.pexels.com/' in image.get_attribute('src')) \
						and (".jpeg" in image.get_attribute("src")) \
						and ("profile" not in image.get_attribute("src")) \
						and	("users" not in image.get_attribute("src")) \
						and ("avatars" not in image.get_attribute("src")):

					urls_tmp.add(image.get_attribute("src"))
			self.driver.execute_script(f"window.scrollTo(0, {pos});")
			time.sleep(1.5)
			pos += 800

		return urls_tmp



scrapGoogle=ScraperGoogle(what_to_scrap="dog",max_fetches=100,
						  folder_path="/home/vladislav/PycharmProjects/tftest/dogs/")

scrapPixabay=ScraperPixabay(what_to_scrap="cat",max_fetches=100,
						  folder_path="/home/vladislav/PycharmProjects/tftest/dogs/")

scrapUnsplash=UnsplashScrapper(what_to_scrap="bee",max_fetches=100,
						folder_path="/home/vladislav/PycharmProjects/tftest/dogs/")

scrapPexels=PexelsScrapper(what_to_scrap="car",max_fetches=100,
						   folder_path="/home/vladislav/PycharmProjects/tftest/dogs/")


if "__main__" == "__main__":

	from multiprocessing import Process

	def run(scraperObj):
		#activate scraping
		scraperObj.run()

	def start_scraping():

		processes = []

		for scraper in (scrapPexels,scrapPixabay,scrapGoogle,scrapUnsplash):
			process=Process(target=run,args=(scraper,))
			processes.append(process)
			process.start()
		for process in processes:
			
			process.join()

	start_scraping()