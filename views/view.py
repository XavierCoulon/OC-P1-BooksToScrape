
from PySide6.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout
from pathlib import Path


class App(QWidget):

	def __init__(self, controller):
		super().__init__()
		self.controller = controller
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
		btn_launch.clicked.connect(self.launch)
		layout.addWidget(btn_launch)

	def get_directory(self):
		response = QFileDialog.getExistingDirectory(self)
		self.field.setText(response)
		return self.field.text()

	def launch(self):
		self.controller.run(self.field.text())


if __name__ == "__main__":
	pass
