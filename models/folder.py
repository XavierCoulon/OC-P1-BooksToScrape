from pathlib import Path


class Folder:

	def __init__(self, path, name):
		self.name = Path(path) / name

	def create(self):
		self.name.mkdir(exist_ok=True)
