import csv
import re
import requests
from pprint import pprint
from pathlib import Path
from text_to_num import text2num
from bs4 import BeautifulSoup
from datetime import datetime

URL = "http://books.toscrape.com/"


def extract_categories():
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html.parser")
    categories_list = []
    categories_tags = soup.find_all("a", href=re.compile("/category/books/"))
    for tag in categories_tags:
        categories_list.append(URL + tag["href"])
    print(f"{len(categories_list)} catégories répertoriées.")

    return categories_list


def extract_books_from_category(category_url_index):
    r = requests.get(category_url_index)
    soup = BeautifulSoup(r.content, 'html.parser')
    category_name = soup.find(class_="page-header action").find("h1").string

    # Seek for the number of additional pages to scrap
    number_additional_pages = int(soup.find(class_="form-horizontal").find("strong").string) // 20

    # Initialize list of category's urls, adding index
    category_url_list = [category_url_index]
    for i in range(number_additional_pages):
        category_url_list.append(category_url_index.replace("index.html", f"page-{i + 2}.html"))
    pprint(f"{len(category_url_list)} pages to be extracted in {category_name} (including index.html).")

    # Initialize list of books in the category
    category_books_list = []
    for category_url in category_url_list:
        print(f"{category_url} in progress...")
        r = requests.get(category_url)
        soup = BeautifulSoup(r.content, "html.parser")
        for tag in soup.find_all(href=re.compile("index"), title=True):
            category_books_list.append(tag["href"].replace("../../..", "http://books.toscrape.com/catalogue"))
    print(f"{len(category_books_list)} books found in {category_name}.")

    return category_books_list


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
    product_description = soup.find("p", class_="")
    # if tag not found / to implement for all extracts ?
    # replace ; by . to avoid Excel issue in csv file - to be checked
    book_information["product_description"] = product_description.string.replace(";", ".") if product_description else ""

    # Extract Image URL
    image_url = soup.find(alt=title).attrs["src"]
    image_url = image_url.replace("../../", URL)
    book_information["image_url"] = image_url

    # Download image
    download_pic(image_url, title.replace("/", "-"))

    # pprint(f"{title} extracted")

    return book_information


def create_csv_file(category_books_list, file_name):
    p = Path.cwd()
    p = p / "CSV"
    p.mkdir(exist_ok=True)
    file_name = f"{file_name}.csv"
    file_to_open = p / file_name
    headers = ["UPC", "product_page_url", "price_excluding_tax", "price_including_tax", "number_available", "title",
               "review_rating", "category", "product_description", "image_url"]
    with open(file_to_open, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(category_books_list)
        print(f"Fichier {file_name} créé sous /CSV.")


def download_pic(image_url, file_name):
    p = Path.cwd()
    p = p / "IMG"
    p.mkdir(exist_ok=True)
    image_name = f"{file_name}.jpg"
    file_to_create = p / image_name
    image = requests.get(image_url).content
    with open(file_to_create, "wb") as handler:
        handler.write(image)


def main():
    categories_list = extract_categories()
    nb_books = 0
    start_time = datetime.now()
    for category_url_index in categories_list:
        category_all_books_information = []
        category_books = extract_books_from_category(category_url_index)
        for book in category_books:
            category_all_books_information.append(extract_book_information(book))
        nb_books += len(category_all_books_information)
        create_csv_file(category_all_books_information, category_all_books_information[0]["category"])
    print(f"{nb_books} books found.")
    print(datetime.now() - start_time)


main()

# pprint(extract_book_information("http://books.toscrape.com/catalogue/shtum_733/index.html"))
# liste = []
# liste.append(extract_book_information("http://books.toscrape.com/catalogue/shtum_733/index.html"))
# pprint(liste)
# create_csv_file(liste, "test")

# download_pic("https://books.toscrape.com/media/cache/63/62/63623a0b014b1f26e49aa61786e6e708.jpg", "test")
