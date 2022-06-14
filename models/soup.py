import requests
from bs4 import BeautifulSoup


class Soup:

	def __init__(self, url):
		self.url = url

	def get(self):
		"""
		Returns:
			BeautifulSoup instance
		"""
		r = requests.get(self.url)
		if r.status_code != 200:
			print(f"Ping {self.url} KO.")
		return BeautifulSoup(r.content, "html.parser")
