#Wallpapers program with classes
#created by Alex Ritchie
from bs4 import BeautifulSoup
import urllib2, random, re, os
from time import sleep
class WallpaperGetter:
	
	def __init__(self,sLocation):
		"""
		sLocation = save location on device
		searchType = 1: keyword, searchType = 2: in-site random, searchType = 3: 
		dictionary random
		"""
		self.keyWord = 'Random'
		self.promptSearchType()
		self.promptNumPics()
		if self.searchType == 1:
			self.promptKeyword()
		elif self.searchType == 2:
			self.dLocation = 'no dictionary'
		else:
			self.promptDictionaryLocation()
		self.setSaveLocation(sLocation)
	def promptNumPics(self):
		self.count = int(raw_input('How many pics to get?'))
	def promptKeyword(self):
		self.keyWord = raw_input("Please enter a key word to search for: ")	
	def promptSearchType(self):
		while True:
			try:
				os.system( [ 'clear', 'cls'][os.name == 'nt'] )
				print 'Main Menu'
				print '1. Enter a keyword'
				print '2. Get a random wallpaper'
				print '3. Get a random wallpaper(based on random dictionary word)'
				print '4. Quit'
			
				result = int(raw_input(""))
				if result == 1: 
					self.searchType = 1
					return
					
				elif result == 2:
					self.searchType = 2
					return			
				elif result == 3: 
					self.searchType = 3
					return
				elif result == 4: exit(0)
				else: raise ValueError
			except ValueError:
				print "not a valid choice"
				sleep(2)
				continue	
					
	def getKeyword(self):
		return self.keyWord
	def promptDictionaryLocation(self):
		self.dLocation = raw_input("What location is your dictionary file?")
	
	def setSaveLocation(self,sLocation):
		self.saveLocation = sLocation
	
	def getNumPics(self):
		return self.numPics
	
	def getDictionaryLocation(self):
		return self.dLocation
	
	def getSaveLocation(self):
		return self.saveLocation
class FourWalledGetter(WallpaperGetter):
	def search(self):
		self.bufCount = 1
		
		#search_type 1 = random, 2 = random dictionary word, 3 = keyword
		while self.bufCount <= self.count:
			self.walledHtml = urllib2.build_opener()
			self.walledHtml.addheaders =[('Referer','http://4walled.cc')]
			self.keyWord1 = self.keyWord
			if self.searchType == 1:
				self.pageSource = self.walledHtml.open('http://4walled.cc/search.php?tags=%s&board=&width_aspect=&searchstyle=larger&sfw=&search=search' %self.keyWord)
			elif self.searchType == 3:
				self.dictionaryTxt = open(self.getDictionaryLocation(),'r')
				self.words = []
				for word in self.dictionaryTxt: self.words.append(word)
				self.dictionaryTxt.close()
				random.shuffle(self.words)
				self.words[0] = self.words[0].replace('\n', '')
				self.keyWord = self.words[0]
				self.pageSource = self.walledHtml.open('http://4walled.cc/search.php?tags='+self.keyWord+'&board=&width_aspect=&searchstyle=larger&sfw=&search=search')
			elif self.searchType == 2:
				self.pageSource = self.walledHtml.open('http://4walled.cc/search.php?tags='+self.keyWord+'&board=&width_aspect=&searchstyle=larger&sfw=&search=search')
								
			self.wallSoup = BeautifulSoup(self.pageSource,"lxml")
			self.downloadAndSave()
			self.bufCount +=1
		
	def downloadAndSave(self):
		if self.searchType == 1: self.warn = False
		if re.match(r'.*?rageface.png$',self.wallSoup.ul.img.get('src')):
			print "Nothing found for "+self.keyWord+"."
			#displays this image when no matches are found.
			if self.searchType == 1: exit(0)
			return
		self.imageList = self.wallSoup.find(id="imageList").find_all("li")
		
		if self.searchType == 2 or self.searchType == 3:
			random.shuffle(self.imageList) #randomizes the list of images 
			self.contents = self.walledHtml.open(self.imageList[-1].a.get('href'))
		elif self.searchType == 1 and self.count > len(self.imageList) and self.warn == False:
			print "Only found "+str(len(self.imageList))+ " pictures. Changing number of pictures to get to "+str(len(self.imageList))+"."
			self.count = len(self.imageList)
			self.warn = True
		if self.searchType == 1:
			self.contents = self.walledHtml.open(self.imageList[self.bufCount].a.get('href'))
		#imageHtml = urllib2.urlopen(imageList[0].a.get('href'))#grabs the first image in randomized list
		self.imageSoup = BeautifulSoup(self.contents,"lxml") #makes beautifulsoup out of imageHtml
		#fileToDl.addheaders = [('Referer', imageList[0].a.get('href'))] #necessary to download
		self.walledHtml = self.walledHtml.open(self.imageSoup.img.get('src'))#opens the picture
		self.fileExt = str(self.imageSoup.img.get('src')).split('.')[-1] #
		os.chdir(os.path.expanduser(self.getSaveLocation()))
		self.found = False
		self.yetAnotherBufCount = self.bufCount
		while True: #this loop searches for duplicate files. If any are found it 
		#changes the name of the search_term(which is the name of the file to be saved)
			if os.path.isfile(self.keyWord1+'.'+self.fileExt):
				self.found = True
			else: break
			if self.found == True:
				self.keyWord1 = self.keyWord + str(self.yetAnotherBufCount)
				self.yetAnotherBufCount += 1
				continue
			
		print 'Writing file '+self.keyWord1 +'.'+ self.fileExt+' \nFile '+str(self.bufCount)+ ' of '+str(self.count)+'.'
		self.localFile = open(self.keyWord1+'.'+self.fileExt,'wb')
		self.localFile.write(self.walledHtml.read())
		self.localFile.close()
		
	
	
		
j = FourWalledGetter('~/Pictures/wallpapers2') #change location to download in a different save location
j.search()
