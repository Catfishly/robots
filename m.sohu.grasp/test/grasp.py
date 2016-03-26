#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
test grasp function add test beautifulsoup
'''
import urllib2
import os
import BeautifulSoup
import re
import sys #used for test

try:
	url=sys.argv[1]
except IndexError,e:
	url='http://m.sohu.com'
#only one *.html: main.html
def getContent(url):
	content=urllib2.urlopen(url).read()
	content=writeCss(url,content)
	content=writefileName(url,content)
	content=writeJs(url,content)
	'''
	#change url to absolute url
	soup=BeautifulSoup.BeautifulSoup(content)
	list_a=soup.findAll('a')
	list_link=soup.findAll('link')
	http_pat=re.compile('href=\"(.*?)\"')
	for i in list_a+list_link:
		url_find= re.findall(http_pat,str(i))
		if url_find!=[]:
			url_find=url_find[0]
		else:
			continue
		print url_find
		if not url_find.startswith('http'):
			content.replace(url_find,url+'/'+url_find)
			print url+"/"+url_find
	'''
	#save main.html to corrent dir
	fileName="main.html"
	f=file(fileName,'w')
	f.write(content)
	f.close()

#only one *.css: home.css
def writeCss(url,content):
	soup=BeautifulSoup.BeautifulSoup(content)
	csss=soup.findAll('link',attrs={'type':'text/css'})
	if len(csss)==0:
		return content
	cssname_pat=re.compile('.*/(.*?)\.css')
	cssurl_pat=re.compile('.*href=\"(.*?)\"')
	css_dir="css/"
	if not os.path.isdir(css_dir):
		os.mkdir(css_dir)
	for css in csss:
		try:
			cssname=re.findall(cssname_pat,str(css))[0]
			cssurl=re.findall(cssurl_pat,str(css))[0]
			css_content=urllib2.urlopen(cssurl).read()
			#mkdir to save .css
			cssname_new=css_dir+cssname+'.css'
			cssfile=file(cssname_new,'w')
			cssfile.write(css_content)
			cssfile.close()
			#change absoute url 
			content=content.replace(cssurl,cssname_new)
		except IndexError,e:
			continue
	return content

def writefileName(url,content):
	soup=BeautifulSoup.BeautifulSoup(content)
	imgs=soup.findAll('img')
	'''print imgs
	sys.exit(111)'''
	if len(imgs)==0:return content
	#two types of img:jpg/png
	original_imgname_pat=re.compile('.*/')
	original_imgurl_pat=re.compile('original=\"(.*?)\"')
	imgname_pat=re.compile('.*/')
	imgurl_pat=re.compile('src=\"(.*?)\"')
	img_dir='images/'
	if not os.path.isdir(img_dir):
		os.mkdir(img_dir)
	for img in imgs:
		try:
			#print img
			if 'original' in str(img):
				imgurl=re.findall(original_imgurl_pat,str(img))[0]
				imgname=imgurl[len(re.findall(original_imgname_pat,imgurl)[0]):len(imgurl)]
			else:
				imgurl=re.findall(imgurl_pat,str(img))[0]
				imgname=imgurl[len(re.findall(imgname_pat,imgurl)[0]):len(imgurl)]
			#print imgurl
			img_content=urllib2.urlopen(imgurl).read()
			imgname_new=img_dir+imgname
			imgfile=file(imgname_new,'w')
			imgfile.write(img_content)
			imgfile.close()
			#change url
			content=content.replace(imgurl,imgname_new)
		except IndexError,e:
			continue
	return content

#save js
def writeJs(url,content):
	soup=BeautifulSoup.BeautifulSoup(content)
	jss=soup.findAll('script',attrs={'type':'text/javascript'})
	if len(jss)==0:return content
	js_dir='js/'
	if not os.path.isdir(js_dir):
		os.mkdir(js_dir)
	jsname_pat=re.compile('src.*/(.*?)\"')
	jsurl_pat=re.compile('src=\"(.*?)\"')
	for js in jss:
		if not '.js' in str(js):
			continue
		try:
			jsname=re.findall(jsname_pat,str(js))[0]
			jsurl=re.findall(jsurl_pat,str(js))[0]
			js_content=urllib2.urlopen(jsurl).read()
			jsname_new=js_dir+jsname
			jsfile=file(jsname_new,'w')
			jsfile.write(js_content)
			jsfile.close()
			#change url
			content=content.replace(jsurl,jsname_new)
		except IndexError,e:
			continue
	return content
if __name__=='__main__':
    getContent(url)
