from selenium.webdriver import Chrome
import bs4

DRIVER_PATH = '/usr/local/bin/chromedriver'
browser = Chrome(executable_path=DRIVER_PATH)

def medium():

	wd = Chrome()
	wd.get('https://google.com')
	search_box = wd.find_element_by_css_selector('input.gLFyf')
	search_box.send_keys('Dogs')

def tmp():
	browser.get('https://duckduckgo.com')
	search_form = browser.find_element_by_id('search_form_input_homepage')
	search_form.send_keys("real_python")
	search_form.submit()
	results = browser.find_elements_by_class_name('result')
	print(results[1].text)
	browser.close()
	quit()

def music():
	browser.get('https://bandcamp.com')
	browser.find_element_by_class_name('play-btn').click()

	tracks = browser.find_elements_by_class_name('discover-item')
	len(tracks)  # 8
	tracks[3].click()

	next_button=[e for e in browser.find_elements_by_class_name("item-page") if e.text.lower().find('next') > -1]
	next_button.click()








