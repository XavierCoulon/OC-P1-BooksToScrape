from module import *
from datetime import datetime


def main():
    """ Main

    1. Scrape all categories fron index page
    2. For

    Returns:

    """
    # to comment
    nb_books_scraped = 0
    start_time = datetime.now()

    for category_url_index in scrape_categories():
        category_all_books_data = []
        category_books = scrape_books_from_category(category_url_index)
        for book in category_books:
            category_all_books_data.append(scrape_book_data(book))
        nb_books_scraped += len(category_all_books_data)
        create_csv_file(category_all_books_data, category_all_books_data[0]["category"])

    print(f"{nb_books_scraped} books extracted.")
    print(datetime.now() - start_time)


# main()
pprint(scrape_book_data("https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"))