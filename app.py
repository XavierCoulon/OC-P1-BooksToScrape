import sys
import main
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout
from pathlib import Path


class App(QWidget):

	singleton = None

	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()
		self.setLayout(layout)
		self.setWindowTitle("Books To Scrape")
		self.setFixedWidth(600)

		btn_browse = QPushButton("1. Sélectionner le dossier")
		btn_browse.clicked.connect(self.get_directory)
		layout.addWidget(btn_browse)

		self.field = QLabel(str(Path.cwd()))
		self.field.setStyleSheet("border: 1px solid blue;")
		layout.addWidget(self.field)

		btn_launch = QPushButton("2. Lancer le scraping")
		btn_launch.clicked.connect(main.run)
		layout.addWidget(btn_launch)

	def get_directory(self):
		response = QFileDialog.getExistingDirectory(self)
		self.field.setText(response)
		return self.field.text()


if __name__ == "__main__":
	appli = QApplication(sys.argv)
	win = app.App()
	app.App.singleton = win
	win.show()
	appli.exec()
