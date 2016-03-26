#!/usr/bin/python
#coding:utf-8
import qiubai
import sys
from random import random
import time
from qiubai import setDelimiter
def sleep():
    #s=float('%.2f'%(random()*10))
    time.sleep(1+random())
'''
def urlGenerator():
    modelUrl='http://www.qiushibaike.com/hot/page/'
    urlList=[]
    for i in range(35):
        url=modelUrl+str(i+1)
        urlList.append(url)
    return urlList
'''
def qiubaiInsert():
    pageCount=0
    startPage=raw_input('input start page number (1~300,default: 1):')
    if not startPage:
        startPage=1
    else:
        startPage=int(startPage)
    endPage=raw_input('input end page number (1~300 default: 300):')
    if not endPage:
        endPage=300
    else:
        endPage=int(endPage)
    print startPage,endPage
    password=raw_input('DB password:')
    countDict={}
    countDict['successNum']=0
    countDict['failureNum']=0
    countDict['totalNum']=0
    #urlList=urlGenerator()
    modelUrl='http://www.qiushibaike.com/hot/page/'
    while True:
        if startPage<=endPage:
            pass
        else:
            break
        url=modelUrl+str(startPage)
        setDelimiter('page:[%s]'%startPage)
        (t,s,f)=qiubai.readArticle(password=password,url=url)
        startPage+=1
        pageCount+=1
        if t==0:
            break
        countDict['successNum']+=s
        countDict['failureNum']+=f
        countDict['totalNum']+=t
        sleep()
        '''
    for url in urlList:
        (t,s,f)=qiubai.readArticle(password=password,url=url)
        if t==0:
            print
        countDict['successNum']+=s
        countDict['failureNum']+=f
        countDict['totalNum']+=t
        '''
    print countDict
    print 'pageCount:',pageCount
if __name__=='__main__':
    qiubaiInsert()
    '''
    urlList=urlGenerator()
    for url in urlList:
        print url'''
