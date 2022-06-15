import views.view
import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication
from multiprocessing import Pool

from models.category import Category
from models.url import Booktoscrape
from models.folder import Folder
from models.constants import URL, CSV_FOLDER, IMG_FOLDER


class Controller:
	img_folder = None
	csv_folder = None

	def setup(self):
		app = QApplication(sys.argv)
		win = views.view.App(controller=self)
		win.show()
		app.exec()

	def create_folders(self, folder):
		self.csv_folder = Folder(path=folder, name=CSV_FOLDER)
		self.csv_folder.create()
		self.img_folder = Folder(path=folder, name=IMG_FOLDER)
		self.img_folder.create()

	def scrape_category(self, category_main_url):
		# number_books_scraped_in_category = 0
		category = Category(index_url=category_main_url)
		category.get_data()
		for book in category.books:
			book.download_pic(self.img_folder.name)
			# number_books_scraped_in_category += 1
		category.create_csv(self.csv_folder.name)

		# return number_books_scraped_in_category

	def run(self, folder):

		number_total_books_scraped = 0
		start_time = datetime.now()
		self.create_folders(folder)

		url = Booktoscrape(url=URL)
		url.get_categories()

		p = Pool()
		p.map(self.scrape_category, url.categories_urls)

		# print(f"{number_total_books_scraped} books extracted.")
		print(datetime.now() - start_time)


if __name__ == "__main__":
	controller = Controller()
	controller.setup()
