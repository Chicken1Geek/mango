class CannotRetriveImage(Exception):
	def __init__(self,message):
		super().__init__(f'Error downloading Image : {message}')

class ErrorGettingMangaData(Exception):
	def __init__(self,message):
		super().__init__(f'Error Getting Manga Data : {message}')