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

		# Identify product table in the page
		product_table = soup.find(class_="table table-striped")
		product_information = product_table.find_all("td")

		# Extract UPC from product table
		self.upc = str(product_information[0].string)

		# Extract price excluding tax from product table
		self.price_excluding_tax = str(product_information[2].string)

		# Extract price including tax from product table
		self.price_including_tax = str(product_information[3].string)

		# Extract availability from product table
		self.number_available = "".join(x for x in product_information[5].string if x.isdigit())

		# Extract Title
		title = soup.find(class_="col-sm-6 product_main").h1.string
		self.title = title

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
		# book_data["product_description"] = product_description.string if product_description else ""

		# Extract Image URL
		image_url = soup.find(alt=title).attrs["src"]
		image_url = image_url.replace("../../", URL)
		self.image_url = image_url
		if image_url == "":
			print(f"{title} in {self.category}")
			return

		# Set file_name
		self.image_name = self.title.replace("/", "-") + "-" + self.upc

	def download_pic(self, folder):

		image_name = f"{self.image_name}.jpg"
		file_to_create = folder / image_name
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
