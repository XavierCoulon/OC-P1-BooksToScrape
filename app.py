import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout
from main import run


class App(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()
		self.setLayout(layout)
		self.setWindowTitle("Books To Scrape")
		self.setFixedWidth(600)

		btn_browse = QPushButton("1. Sélectionner le dossier")
		btn_browse.clicked.connect(self.get_directory)
		layout.addWidget(btn_browse)

		self.field = QLabel()
		self.field.setStyleSheet("border: 1px solid blue;")
		layout.addWidget(self.field)

		btn_launch = QPushButton("2. Lancer le scraping")
		btn_launch.clicked.connect(run)
		layout.addWidget(btn_launch)

	def get_directory(self):
		response = QFileDialog.getExistingDirectory(
			self,
			caption="Sélectionnez un répertoire",
		)
		self.fill_field(response)

	def fill_field(self, value):
		self.field.setText(value)


app = QApplication(sys.argv)
win = App()
win.show()
app.exec()
