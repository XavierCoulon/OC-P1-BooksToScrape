import sys
import views.view

from multiprocessing import Pool
from datetime import datetime
from PySide6.QtWidgets import QApplication

from models.book import Book
from models.category import Category
from models.url import Url, URL
from models.folder import Folder


class Controller:

    # win = None

    def setup(self):
        app = QApplication(sys.argv)
        win = views.view.App(controller=self)
        # self.win = win
        win.show()
        app.exec()

    @staticmethod
    def scrape(folder):

        nb_books_scraped = 0
        start_time = datetime.now()
        csv_folder = Folder(path=folder, name="CSV")
        csv_folder.set_folder()
        img_folder = Folder(path=folder, name="IMG")
        img_folder.set_folder()

        url = Url(url=URL)
        url.get_categories()
        for category_main_url in url.categories_url:

            category = Category(main_url=category_main_url)
            category.load_data()
            for book in category.books:
                book.download_pic(img_folder.name)
                nb_books_scraped += 1

            category.csv(csv_folder.name)

        print(f"{nb_books_scraped} books extracted.")
        print(datetime.now() - start_time)


if __name__ == "__main__":
    controller = Controller()
    controller.setup()

