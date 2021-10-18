import csv
import re
import requests
from pprint import pprint
from pathlib import Path
from text_to_num import text2num
from bs4 import BeautifulSoup


URL = "http://books.toscrape.com/"


def scrape_categories():
    """ Scrape categories URLs from the nav list books

    Returns:
        categories_urls_list (list): URLs of all categories

    """

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html.parser")
    categories_urls_list = []
    categories_nav_list = soup.find(class_="nav nav-list").ul.find_all("a")
    for category in categories_nav_list:
        categories_urls_list.append(URL + category["href"])
    print(f"{len(categories_urls_list)} catégories répertoriées.")

    return categories_urls_list


def scrape_books_from_category(category_url_index):
    """ Scrape URLs of all books of a category (index + additional pages)

    Args:
        category_url_index (str): url of the index page (of a dedicated category)

    Returns:
        books_urls_list (list): URLs of all books of the category
    """

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
    books_urls_list = []
    for category_url in category_url_list:
        print(f"{category_url} in progress...")
        r = requests.get(category_url)
        soup = BeautifulSoup(r.content, "html.parser")
        for tag in soup.find_all(href=re.compile("index"), title=True):
            books_urls_list.append(tag["href"].replace("../../..", "http://books.toscrape.com/catalogue"))
    print(f"{len(books_urls_list)} books found in {category_name}.")
    pprint(books_urls_list)

    return books_urls_list


def scrape_book_data(book_page_url):
    """ Scrape data from book index page

    Args:
        book_page_url (str): index page of a book

    Returns:
        book_data (dict): data of the book (UPC, price excluding tax,...)

    """
    book_data = {
        "product_page_url": book_page_url
    }
    r = requests.get(book_page_url)
    if r.status_code != 200:
        print(f"Ping {book_page_url} KO.")
        return

    soup = BeautifulSoup(r.content, 'html.parser')

    # Identify product table in the page
    product_table = soup.find(class_="table table-striped")
    product_information = product_table.find_all("td")

    # Extract UPC from product table
    book_data["UPC"] = product_information[0].string

    # Extract price excluding tax from product table
    book_data["price_excluding_tax"] = product_information[2].string

    # Extract price including tax from product table
    book_data["price_including_tax"] = product_information[3].string

    # Extract availability from product table
    book_data["number_available"] = "".join(x for x in product_information[5].string if x.isdigit())

    # Extract Title
    title = soup.find(class_="col-sm-6 product_main").h1.string

    # Extract review rating
    # Using tag's attributes to look for the rate, then convert to integer (using text2num)
    tag = soup.find("p", re.compile("star-rating")).attrs["class"][1]
    book_data["review_rating"] = text2num(tag.lower(), "en")

    # Extract Category
    breadcrumb = soup.find(class_="breadcrumb")
    links = breadcrumb.find_all("a")
    book_data["category"] = links[2].string

    # Extract Product Description
    product_description = soup.find("p", class_="")
    # if tag not found / to implement for all extracts ?
    # replace ; by . to avoid Excel issue in csv file - to be checked
    book_data["product_description"] = product_description.string.replace(";", ".") \
        if product_description else ""

    # Extract Image URL
    image_url = soup.find(alt=title).attrs["src"]
    image_url = image_url.replace("../../", URL)
    book_data["image_url"] = image_url

    # Download image
    download_pic(image_url, title.replace("/", "-"))

    return book_data


def create_csv_file(category_all_books_data, file_name):
    """ Create a csv file

    Args:
        category_all_books_data (list): list of X dictionnaries, one dictionnay gathering data from one book
        file_name (str): name of the CSV file (= category)

    Returns:
        empty list

    """
    p = Path.cwd()
    p = p / "CSV"
    p.mkdir(exist_ok=True)
    file_name = f"{file_name}.csv"
    file_to_open = p / file_name
    headers = ["UPC", "product_page_url", "price_excluding_tax", "price_including_tax", "number_available", "title",
               "review_rating", "category", "product_description", "image_url"]
    with open(file_to_open, "w", newline="", encoding="utf-8-sig") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(category_all_books_data)
        print(f"Fichier {file_name} créé sous /CSV.")

    return []


def download_pic(image_url, file_name):

    # TO DO - Add a check if path already exists
    p = Path.cwd()
    p = p / "IMG"
    p.mkdir(exist_ok=True)
    image_name = f"{file_name}.jpg"
    file_to_create = p / image_name
    image = requests.get(image_url).content
    with open(file_to_create, "wb") as f:
        f.write(image)


# __name__ to test only a sample:
# 1 . Scrape all catogories,
# 2 . Scrape all books from 1 category,
# 3. Scrape data for 1 book
# 4. Save csv file for dedicated book (__name__.csv)
# 4. Download pic for dedicated book (__name__jpg)

if __name__ == "__main__":
    pprint(scrape_categories())
    print("""\n""")
    pprint(scrape_books_from_category("https://books.toscrape.com/catalogue/category/books/romance_8/index.html"))
    print("""\n""")
    book_test = scrape_book_data("https://books.toscrape.com/catalogue/chase-me-paris-nights-2_977/index.html")
    pprint(book_test)
    print("""\n""")
    liste = [book_test]
    create_csv_file(liste, "__name__")
    print("""\n""")
    download_pic("https://books.toscrape.com/media/cache/6c/84/6c84fcf7a53b02b6e763de7272934842.jpg", "__name__")
