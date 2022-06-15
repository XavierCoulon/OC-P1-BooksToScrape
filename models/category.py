import re
import csv

from models.soup import Soup
from models.book import Book
from models.constants import HEADERS, CSV_FOLDER, URL


class Category:
	name = None
	soup = None
	index_url = None
	additional_urls = []
	books = []

	def __init__(self, index_url):
		self.index_url = index_url
		self.soup = Soup(self.index_url).get()

	def get_data(self):

		# Get name
		self.name = self.soup.find(class_="page-header action").find("h1").string

		# Seek for the number of additional pages to run
		number_additional_pages = int(self.soup.find(class_="form-horizontal").find("strong").string) // 20

		# Build additional_urls from number_additional_pages
		self.additional_urls = [
			self.index_url.replace("index.html", f"page-{i + 2}.html") for i in range(number_additional_pages)]
		print(f"{len(self.additional_urls) + 1} pages to be extracted in {self.name} (including index.html).")

		# Initialize list of books in the category
		for url in self.additional_urls + [self.index_url]:
			soup = Soup(url).get()
			for tag in soup.find_all(href=re.compile("index"), title=True):
				book = Book(product_page_url=tag["href"].replace("../../..", f"{URL}catalogue"))
				book.get_data()
				self.books.append(book)
		print(f"{len(self.books)} book(s) found in {self.name}.")

	def create_csv(self, folder):

		file_name = f"{self.name}.csv"
		file_to_open = folder / file_name
		with open(file_to_open, "w", newline="", encoding="utf-8-sig") as output_file:
			writer = csv.DictWriter(output_file, fieldnames=HEADERS)
			writer.writeheader()
			for book in self.books:
				writer.writerow(book.serialize())
			print(f"Fichier {file_name} créé sous /{CSV_FOLDER}.")
