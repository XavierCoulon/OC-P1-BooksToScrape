import re, csv

from models.soup import Soup
from pathlib import Path


class Category:

	def __init__(self, index):
		self.index = index
		self.additional_urls = []
		self.books_urls = []
		self.all_books_data = []
		self.name = None

	def get_category_data(self):
		soup = Soup(self.index).get_soup()

		# Get name
		self.name = soup.find(class_="page-header action").find("h1").string

		# Seek for the number of additional pages to scrape
		number_additional_pages = int(soup.find(class_="form-horizontal").find("strong").string) // 20

		# Initialize list of category's urls, adding index.html
		for i in range(number_additional_pages):
			self.additional_urls.append(self.index.replace("index.html", f"page-{i + 2}.html"))
		print(f"{len(self.additional_urls)} pages to be extracted in {self.name} (including index.html).")

		# Initialize list of books in the category
		for url in self.additional_urls + [self.index]:
			soup = Soup(url).get_soup()
			for tag in soup.find_all(href=re.compile("index"), title=True):
				self.books_urls.append(tag["href"].replace("../../..", "http://books.toscrape.com/catalogue"))
		print(f"{len(self.books_urls)} book(s) found in {self.name}.")

	def csv(self):

		p = Path.cwd()
		p = p / "CSV"
		p.mkdir(exist_ok=True)
		file_name = f"{self.name}.csv"
		file_to_open = p / file_name
		headers = ["UPC", "product_page_url", "price_excluding_tax", "price_including_tax", "number_available", "title", "review_rating", "category", "product_description", "image_url"]
		with open(file_to_open, "w", newline="", encoding="utf-8-sig") as output_file:
			writer = csv.DictWriter(output_file, fieldnames=headers)
			writer.writeheader()
			writer.writerows(self.all_books_data)
			print(f"Fichier {file_name} créé sous /CSV.")
