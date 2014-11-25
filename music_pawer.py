# coding=utf-8
import HTMLParser
from bs4 import BeautifulSoup
import urllib
import urllib2
import socket 
import sys
import dbconfig
import MySQLdb as mdb
from datetime import *
try:

	conn = dbconfig.connectDB()
	cur  = conn.cursor(mdb.cursors.DictCursor)
	
	sql = 'select * from music'
	cur.execute(sql)
	results = cur.fetchall()			
	##qqmusic

	html = urllib.urlopen('http://y.qq.com/y/static/index.html')
	tt = ''
#	for i in range(0, 9):
#		text = html.read(10000)
#		tt += text
#	print tt
	soup = BeautifulSoup(html)

	
	now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	qq_new	= soup.find('ul', {'class':'mod_first_list'})

#	print qq_new	
	for x in qq_new.find_all('li'):	



		a = x.find('a',{'class':'mod_poster_130'})	
		print 'song_url', 'http://y.qq.com' + a.get('href')	
		em = x.find('strong', {'class':'album_name'})
		print 'song', em.contents[0].encode('utf8')
		em = x.find('strong', {'class':'album_singer'})
		print 'singer', em.contents[0].encode('utf8')

                url = 'http://y.qq.com' + a.get('href')
                song =   em.contents[0]
                singer =  em.contents[0]

                source = u'qq'


	        exist = False;
	        for item in results:
        	        if item['song'] == song:
                	        exist = True
	        if not exist:
        	        sql = 'insert into music (url, song, singer, source, date) values ("%s", "%s", "%s", "%s", "%s")' % (url, song, singer, source, now)
	                cur.execute(sql)
        	        conn.commit()
	#xiami 
	url = 'http://www.xiami.com'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	values = {'name' : 'Michael Foord',
    	      'location' : 'Northampton',
        	  'language' : 'Python' }
	headers = { 'User-Agent' : user_agent }
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data, headers)
	response = urllib2.urlopen(req)
	the_page = response.read()	
#	print the_page
	soup = BeautifulSoup(the_page)

	xiami_new	= soup.find('div', {'id':'albums'})
#	print xiami_new
	info = xiami_new.find('div',{'class':'album'})				
	#print info
	a = info.find('div',{'class':'info'})	
	p = a.find_all('p')	
	

	url = 'http://www.xiami.com' +p[0].find('a').get('href')
	song =  p[0].find('a').string.encode('utf8')
	singer =  p[1].find('a').string.encode('utf8')
	source = u'xiami'
	print 'song_url' , 'http://www.xiami.com' +p[0].find('a').get('href')
	print 'song', p[0].find('a').string.encode('utf8')
	print 'singer', p[1].find('a').string.encode('utf8')
	exist = False;
	for item in results:
		if item['song'] == song:
			exist = True	
	
	if not exist:
		sql = 'insert into music (url, song, singer, source,date) values ("%s", "%s", "%s", "%s", "%s")' % (url, song, singer, source, now)
		cur.execute(sql)
		conn.commit()

	for sibling in info.next_siblings:
		#print(repr(sibling))
		#break
		if(sibling !=' ' ):
			a = sibling.find('div',{'class':'info'})	
			p = a.find_all('p')	
			#print p
			print 'song_url' , 'http://www.xiami.com' + p[0].find('a').get('href')
			print 'song', p[0].find('a').string.encode('utf8')
			print 'singer', p[1].find('a').string.encode('utf8')


		        url = 'http://www.xiami.com' +p[0].find('a').get('href')
		        song =  p[0].find('a').string
		        singer =  p[1].find('a').string
		        source = 'xiami'
		        print 'song_url' , 'http://www.xiami.com' +p[0].find('a').get('href')
		        print 'song', p[0].find('a').string.encode('utf8')
		        print 'singer', p[1].find('a').string.encode('utf8')
		        exist = False;
		        for item in results:
		                if item['song'] == song:
		                        exist = True
		        if not exist:
		                sql = 'insert into music (url, song, singer, source, date) values ("%s", "%s", "%s", "%s", "%s")' %( url, song, singer, source, now)
		                cur.execute(sql)
		                conn.commit()


	#163

	html = urllib.urlopen('http://music.163.com/discover')
	text =  html.read()
	soup = BeautifulSoup(text)
	#print text
	a	= soup.find('ul', {'class':'f-cb roller-flag'})
	#print a
	for x in a.find_all('li'):	
		p = x.find_all('p')


                url = 'http://music.163.com/#' +p[0].find('a').get('href')
                song =  p[0].find('a').string
                singer =  p[1].find('a').string
                source = '163'
                print 'song_url' , 'http://music.163.com/#' +p[0].find('a').get('href')
                print 'song', p[0].find('a').string.encode('utf8')
                print 'singer', p[1].find('a').string.encode('utf8')
                exist = False;
                for item in results:
			if item['song'] == song:
                        	exist = True
                if not exist:
			sql = 'insert into music (url, song, singer, source, date) values ("%s", "%s", "%s", "%s", "%s")' %( url, song, singer, source, now)
                        cur.execute(sql)
                        conn.commit()







except socket.error, msg:
	print 'error'
conn.close() 
