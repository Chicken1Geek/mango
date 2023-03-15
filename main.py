import pdfTools as tools
import sites
def getManga(url):
	data = sites.getMangaData(url)
	imageList = tools.downloadImages(data[1])
	tools.buildPdf(imageList,'results/'+data[0].id + data[0].chapter + '.pdf')
	tools.removeImages(imageList)
	
getManga('https://manga4life.com/read-online/Ijiranaide-Nagatoro-san-chapter-110.html')