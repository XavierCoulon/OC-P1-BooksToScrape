from pathlib import Path

# FOLDER = "/Users/xco/Desktop"


class Folder:

	def __init__(self, path, name):
		self.name = Path(path) / name

	def set_folder(self):
		self.name.mkdir(exist_ok=True)

