from user_agent import generate_user_agent
from requests import get
import exceptions

def getSite(url : str):
	try:
		print(f'Getting Manga Data for {url}')
		return get(url,headers={'User-Agent':generate_user_agent(device_type='desktop')}).text
	except Exception as e:
		raise exceptions.ErrorGettingMangaData(e)

def getMangaObject(url : str):
	mangaSite = url.split('.')[0].split('://')[1]
	if mangaSite == 'manga4life':
		return manga4life(url)

def getMangaChapterUrl(mangaObject,chapter: int):
	chapter = str(chapter).zfill(4)
	return mangaObject.chapterUrl.replace('<chapter>',chapter)

def getMangaChapter(mangaObject,chapter : int = None):
		result = []
		if chapter == None:
			chapter = mangaObject.chapter
		chapter = str(chapter).zfill(4)
		for page in range(1,mangaObject.pageLength+1):
			page = str(page)
			result.append(mangaObject.imageUrl.replace('<page>',page.zfill(3)).replace('<chapter>',chapter))
		return mangaObject,result

class manga4life:
	def __init__(self,mangaUrl):
		urlContents = mangaUrl.split('.com/')[1].split('/')
		if urlContents[0] != 'manga':
			query = urlContents[1].split('-page-')
			if len(query) == 1:
				query = query[0].split('-chapter-')
				self.id = query[0]
				self.chapter = query[1].strip('.html')
				self.page = 1
			else:
				self.page = query[-1].strip('.html')
				query = query[0].split('-chapter-')
				self.id = query[0]
				self.chapter = query[1].strip('.html')
		else:
			self.id = urlContents[-1]
			self.chapter = 1
			self.page = 1
		mangaUrl = f'https://manga4life.com/read-online/{self.id}-chapter-{self.chapter}.html'
		data = getSite(mangaUrl)
		self.imageCdn = 'https://' + data.split('vm.CurPathName = \"')[1].split('\";')[0]
		self.imageUrl = f'{self.imageCdn}/manga/{self.id}/<chapter>-<page>.png'
		self.pageLength = int(data.split('vm.CurPathName = \"')[0].split('\"Page\":')[1].split('\"')[1])
		self.chapterUrl = mangaUrl.split('-chapter-')[0] + '-chapter-<chapter>.html'
		self.url = mangaUrl

class asurascans:
	def __init__(self,surl):
		curl = surl
		surl = surl.strip('https://www.asurascans.com').split('-chapter-')
		if len(surl) == 2:
			self.id = surl[0]
			self.chapter = surl[1]
			self.page = 1
			self.chapterUrl = curl.replace(self.chapter,'<chapter>')
		else:
			self.id = surl[0]
			self.chapter = 1
			self.page = 1
			self.chapterUrl = curl.strip('/') + '-chapter-<chapter>'
		data = getSite(curl)
		print(data)