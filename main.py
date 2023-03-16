import pdfTools as tools
import sites
from random import randint


def downloadMangaChapter(url : str, chapter : int = None):
	manga = sites.getMangaObject(url)
	if chapter == None:
		chapter = manga.chapter
	data = sites.getMangaChapter(manga,chapter)
	imageList = tools.downloadImages(data[1])
	tools.buildPdf(imageList,'results/'+str(randint(10000,99999))+data[0].id + data[0].chapter + '.pdf')
	tools.removeImages(imageList)

def downloadMangaChapters(url : str, chapters):
	imageList = []
	sourceManga = sites.getMangaObject(url)
	mangas = []
	print(sourceManga.__dict__)
	for chapter in chapters:
		mangas.append(sites.getMangaChapterUrl(sourceManga,chapter))
		
	
	for manga in mangas:
		manga = sites.getMangaObject(manga)
		data = sites.getMangaChapter(manga)
		imageList.extend(tools.downloadImages(data[1]))
	tools.buildPdf(imageList,'results/'+str(randint(10000,99999))+data[0].id + data[0].chapter + '.pdf')
	tools.removeImages(imageList)