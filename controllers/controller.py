from multiprocessing import Pool
from datetime import datetime


from models.book import Book
from models.category import Category
from models.url import Url, URL


def run():

    nb_books_scraped = 0
    start_time = datetime.now()

    url = Url(url=URL)
    url.get_categories()
    for category_index in url.categories_url:

        category = Category(index=category_index)
        category.get_category_data()
        for book_url in category.books_urls:
            book = Book(product_page_url=book_url)
            book.get_book_data()
            category.all_books_data.append(book.serialize())
            nb_books_scraped += 1

        category.csv()

    print(f"{nb_books_scraped} books extracted.")
    print(datetime.now() - start_time)


if __name__ == "__main__":
    run()
