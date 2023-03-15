from user_agent import generate_user_agent
from requests import get


def getMangaData(url : str):
	mangaSite = url.split('.')[0].split('://')[1]
	if mangaSite == 'manga4life':
		manga = manga4life(url)
		result = []
		for page in range(1,manga.pageLength +1):
			page = str(page)
			result.append(manga.imageUrl.replace('<page>',page.zfill(3)))
		return manga,result

class manga4life:
	def __init__(self,mangaUrl):
		urlContents = mangaUrl.split('/')[-1].split('-chapter-')
		self.id = urlContents[0]
		self.chapter = urlContents[1].split('-page-')[0].zfill(4)
		self.chapter = urlContents[1].split('.')[0].zfill(4)
		try:
			print(f'Getting Manga Data for {mangaUrl}')
			data = get(mangaUrl,headers={'User-Agent':generate_user_agent(device_type='desktop')}).text
		except Exception as e:
			raise exceptions.ErrorGettingMangaData(e)
		self.imageCdn = 'https://' + data.split('vm.CurPathName = \"')[1].split('\";')[0]
		self.pageLength = int(data.split('vm.CurPathName = \"')[0].split('\"Page\":')[1].split('\"')[1])
		self.imageUrl = f'{self.imageCdn}/manga/{self.id}/{self.chapter}-<page>.png'