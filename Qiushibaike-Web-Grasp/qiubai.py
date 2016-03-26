#!/usr/bin/python
#coding:utf-8

import urllib
import MySQLdb as mydb
import qiubaiSql
import re
import sys
import urllib2
def setDelimiter(name='-'):
    row=40
    half=(row-len(name))/2
    print '-'*half+name+'-'*half


def login(url='-'):
    setDelimiter('login qiubai')
    setDelimiter('ask for page')
    if url=='-':url='http://www.qiushibaike.com/hot/page/1'
    userAgent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    upgradeInsecureRequest='1'
    headersQiubai={
    'Upgrade-Insecure-Requests':upgradeInsecureRequest,
    'User-Agent':userAgent,}
    try:
        req=urllib2.Request(url,headers=headersQiubai)
        resp=urllib2.urlopen(req)
        #print resp.read()
        setDelimiter('login successfully')
        return resp.read()
    except urllib2.URLError,e:
        if hasattr(e,'code'):
            print e.code
        if hasattr(e,'reason'):
            print e.reason
        return 'login error'
    except ValueError:
        return 'login error'

def findArticles(url='-'):
    setDelimiter('find all articles')
    page=login(url=url)
    #print page
    if page=='login error':
        setDelimiter('url error')
        sys.exit(110)
    pat=re.compile('<div\s?class=\"article.*?\"(?P<article>.*?)<div\s?class=\"single-clear\"></div>.*?</div>',re.S)
    articles=re.findall(pat,page)
    setDelimiter('all articles')
    #print articles
    #for article in articles:
    #    print article
    #print articles[0]
    return articles
def readArticle(password='-',url='http://www.qiushibaike.com/hot/page/3000'):
    failureNum=0
    successNum=0
    setDelimiter('insert article to DB')
    articles=findArticles(url=url)
    totalNum=len(articles)
    #print articles[0]
    #sys.exit(109)
    pat=re.compile(
    'id=[\'\"](?P<articleID>.*?)[\'\"]>.*?'+#articleID
    '<div.*?class="author">.*?<a.*?href=.*?target=.*?>\n<img.*?>(?P<author>.*?)</a>.*?</div>.*?'+#author
    '<div.*?class=\"content\">(?P<content>.*?)<!--(?P<articleTime>\d+)-->.*?</div>.*?'+#content
    '<span\s?class="stats-vote">.*?<i\s?class="number">(?P<stats_vote>.*?)</i>.*?</span>.*?'+#stats-vote
    '<span\s?class="stats-comments">.*?<i\s?class="number">(?P<stats_comments>.*?)</i>.*?</span>'
    ,re.S)
    conn,curs=qiubaiSql.getQiubaiDb(password=password)
    for article in articles:
        #setDelimiter('an article')
        find=re.search(pat,article)
        #print find.group(0)
        #sys.exit(109)
        articleDict={}
        try:
            articleDict['articleId']=find.group('articleID').strip()
            articleDict['author']=find.group('author').strip()
            #tempContent=find.group('content').strip()
            #database improved to sovle the following problem
            #if len(tempContent)>=1200:
            #    tempContent=tempContent[:1200]
            articleDict['content']=find.group('content').strip()
            articleDict['stats_vote']=find.group('stats_vote').strip()
            articleDict['stats_comments']=find.group('stats_comments').strip()
        except AttributeError,e:
            setDelimiter('re fail')
            failureNum+=1
            continue
            #sys.exit(111)
        insertSql="INSERT INTO qiubai VALUES('%s','%s','%s',%s,%s)"%(articleDict['articleId'],articleDict['author'],articleDict['content'],articleDict['stats_vote'],articleDict['stats_comments'])
        #print insertSql
        #print '%s'%articleDict['articleId']
        #sys.exit(109)
        try:
            curs.execute(insertSql)
            successNum+=1
        except curs.IntegrityError:
            failureNum+=1
            continue
        except curs.ProgrammingError:
            failureNum+=1
            continue

        '''
        print 'articleID:',find.group('articleID').strip()
        print 'author:',find.group('author').strip()
        print 'content:',find.group('content').strip()
        print 'stats-vote:',find.group('stats_vote').strip()
        print 'stats-comments:',find.group('stats_comments').strip()
        #sys.exit(109)
        loop=raw_input('continue?[y]/n:')
        if loop!='n':continue
        else: sys.exit(0)
        '''
    conn.commit()
    curs.close()
    conn.close()
    setDelimiter('insert DB down')
    setDelimiter(str(totalNum)+','+str(successNum)+','+str(failureNum))
    return (totalNum,successNum,failureNum)
if __name__=='__main__':
    #login()
    readArticle()
