from module import scrape_categories, scrape_book_data, scrape_books_from_category, create_csv_file
from multiprocessing import Pool
from datetime import datetime
from tqdm import tqdm


def main():
    """ Main script

    1. Scrape all categories from index page
    2. For each category (all pages of the category):
        a. Scrape all books,
            For each book,
                i. Scrape data,
                ii. Download pic,
        b. Create CSV file

    """

    nb_books_scraped = 0
    start_time = datetime.now()

    for category_url_index in scrape_categories():
        # category_all_books_data = []
        category_books = scrape_books_from_category(category_url_index)
        p = Pool()
        category_all_books_data = p.map(scrape_book_data, tqdm(category_books))

        # for book in tqdm(category_books):
        #    category_all_books_data.append(scrape_book_data(book))

        nb_books_scraped += len(category_all_books_data)
        create_csv_file(category_all_books_data, category_all_books_data[0]["category"])

    print(f"{nb_books_scraped} books extracted.")
    print(datetime.now() - start_time)


if __name__ == "__main__":
    main()
