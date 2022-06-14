from models.soup import Soup


class Url:

	def __init__(self, url):
		self.url = url
		self.categories_url = []

	def get_categories(self):
		soup = Soup(self.url).get()
		categories_nav_list = soup.find(class_="nav nav-list").ul.find_all("a")
		self.categories_url = [(self.url + category.get("href")) for category in categories_nav_list]
		print(f"{len(self.categories_url)} catégories répertoriées.")
