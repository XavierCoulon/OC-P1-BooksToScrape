import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QLabel


class App(QWidget):
	def __init__(self):
		super().__init__()
		layout = QHBoxLayout()
		self.setLayout(layout)
		self.setWindowTitle("Books To Scrape")
		self.setFixedWidth(600)

		self.field = QLabel()
		layout.addWidget(self.field)

		btn_browse = QPushButton("Sélectionner le dossier")
		btn_browse.clicked.connect(self.get_directory)
		layout.addWidget(btn_browse)

		btn_launch = QPushButton("Sélectionner le dossier")
		btn_launch.clicked.connect(self.get_directory)
		layout.addWidget(btn_launch)

	def get_directory(self):
		response = QFileDialog.getExistingDirectory(
			self,
			caption="Sélectionnez un répertoire",
		)
		self.field.setText(response)

		return response


app = QApplication(sys.argv)
win = App()
win.show()
app.exec()
