import csv
import re
import requests
from pprint import pprint
from text_to_num import text2num
from bs4 import BeautifulSoup


def extract_book_information(book_page_url):
    book_information = {
        "product_page_url": book_page_url
    }
    r = requests.get(book_page_url)
    if r.status_code != 200:
        print("Ping KO")
        return

    soup = BeautifulSoup(r.content, 'html.parser')

    # Extract UPC
    upc = soup.find("th", string="UPC").next_element.next_element.string
    book_information["UPC"] = upc

    # Extract price excluding tax
    price_excluding_tax = soup.find("th", string="Price (excl. tax)").next_element.next_element.string
    book_information["price_excluding_tax"] = price_excluding_tax

    # Extract price including tax
    price_including_tax = soup.find("th", string="Price (incl. tax)").next_element.next_element.string
    book_information["price_including_tax"] = price_including_tax

    # Extract availability
    number_available = soup.find("th", string="Availability").next_element.next_element.next_element.string
    book_information["number_available"] = "".join(x for x in number_available if x.isdigit())

    # Extract Title
    title = soup.find("li", class_="active").string
    book_information["title"] = title

    # Extract review rating
    # Using tag's attributes to look for the rate, then convert to integer (using text2num)
    tag = soup.find("p", re.compile("star-rating")).attrs["class"][1]
    book_information["review_rating"] = text2num(tag.lower(), "en")

    # Extract Category
    category = soup.find("a", href=re.compile("/category/books/")).string
    book_information["category"] = category

    # Extract Product Description
    product_description = soup.find("p", class_="").string
    book_information["product_description"] = product_description

    # Extract Image URL
    image_url = soup.find(alt=title).attrs["src"]
    book_information["image_url"] = image_url

    return book_information


def create_csv_file(book_information):
    file_name = "data.csv"
    with open(file_name, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=book_information.keys())
        writer.writeheader()
        writer.writerow(book_information)
        print("Fichier créé.")


def main():
    book = extract_book_information("http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html")
    create_csv_file(book)


main()
