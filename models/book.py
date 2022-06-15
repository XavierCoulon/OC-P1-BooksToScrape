import re
import requests

from models.soup import Soup
from text_to_num import text2num
from models.constants import URL


class Book:
	product_page_url = None,
	upc = None
	price_excluding_tax = None
	price_including_tax = None
	number_available = None
	title = None
	review_rating = None
	category = None
	product_description = None
	image_url = None
	image_name = None

	def __init__(self, product_page_url):
		self.product_page_url = product_page_url

	def get_data(self):
		soup = Soup(str(self.product_page_url)).get()

		# Identify product informations in the page
		product_informations = soup.find(class_="table table-striped").find_all("td")

		self.upc = str(product_informations[0].string)
		self.price_excluding_tax = str(product_informations[2].string)
		self.price_including_tax = str(product_informations[3].string)
		self.number_available = "".join(x for x in product_informations[5].string if x.isdigit())
		self.title = soup.find(class_="col-sm-6 product_main").h1.string

		# Extract review rating
		# Using tag's attributes to look for the rate, then convert to integer (using text2num)
		tag = soup.find("p", re.compile("star-rating")).attrs["class"][1]
		self.review_rating = text2num(tag.lower(), "en")

		# Extract Category
		breadcrumb = soup.find(class_="breadcrumb")
		links = breadcrumb.find_all("a")
		# Why needed to apply str ?!?
		self.category = str(links[2].string)

		# Extract Product Description
		product_description = soup.find("p", class_="")
		# if tag not found / to implement for all extracts ?
		# replace ; by . to avoid Excel issue in create_csv file - to be checked
		self.product_description = product_description.string.replace(";", ".") if product_description else ""

		# Extract Image URL
		image_url = soup.find(alt=self.title).attrs["src"]
		self.image_url = image_url.replace("../../", URL)
		if self.image_url == "":
			print(f"{self.title} in {self.category}")
			return

		# Set file_name
		self.image_name = self.title.replace("/", "-") + "-" + self.upc

	def download_pic(self, folder):
		"""
		Using the image_url to download the picture in a specific folder
		Args:
			folder (path): Path (where to download the pic)

		Returns:

		"""
		file_to_create = folder / f"{self.image_name}.jpg"
		image = requests.get(self.image_url).content
		with open(file_to_create, "wb") as f:
			f.write(image)

	def serialize(self):
		return {
			"product_page_url": self.product_page_url,
			"UPC": self.upc,
			"price_excluding_tax": self.price_excluding_tax,
			"price_including_tax": self.price_including_tax,
			"number_available": self.number_available,
			"title": self.title,
			"review_rating": self.review_rating,
			"category": self.category,
			"product_description": self.product_description,
			"image_url": self.image_url
		}
