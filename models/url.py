from models.soup import Soup


class Booktoscrape:

	def __init__(self, url):
		self.url = url
		self.categories_urls = []

	def get_categories(self):
		soup = Soup(self.url).get()
		categories_nav_list = soup.find(class_="nav nav-list").ul.find_all("a")
		self.categories_urls = [(self.url + category.get("href")) for category in categories_nav_list]
		print(f"{len(self.categories_urls)} catégories répertoriées.")
