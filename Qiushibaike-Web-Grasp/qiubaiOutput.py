#!/usr/bin/python
# -*- coding:utf-8 -*-
import xlwt
import sys
import qiubaiSql
from qiubai import setDelimiter
class xlsx(object):
    def __init__(self):
        self.row=0
        self.file=xlwt.Workbook()
    def addSheet(self,name='sheet1'):
        self.sheet=self.file.add_sheet(name,cell_overwrite_ok=True)

    def writeTuple(self,tup):
        for col,t in enumerate(tup):

            #sys.exit(109)
            #if col==1: t=t.decode('gbk')
            #if col==2: t=t.decode('utf-8')
            if type(t)==str:
                try:
                    t=t.decode('utf-8')
                except UnicodeDecodeError,e:
                    try:
                        t=t.decode('gbk')
                    except UnicodeDecodeError,e:
                        t='error encoding'
            self.sheet.write(self.row,col,t)
        self.row+=1
        #def closeWorkbook(self,saveName='qiubai.xls'):
        self.file.save('qiubai.xls')
class database(object):
    def __init__(self):
        self.conn,self.curs=qiubaiSql.getQiubaiDb()
    def readArticles(self):
        self.sql="select * from qiubai"
        self.curs.execute(self.sql)
        return self.curs
    def closeConnection(self):
        self.conn.close()

def writeArticles():
    x=xlsx()
    x.addSheet()
    d=database()
    curs=d.readArticles()
    row=0
    #init title
    title=('ID','Name','Content','good','apply')
    x.writeTuple(title)
    while True:
        #try:
        setDelimiter('row %d'%row)
        tup=curs.fetchone()
        #if row==18: print tup
        #print tup
        #break
        if tup:
            x.writeTuple(tup)
        else:
            break
        row+=1
        #except:
        #    continue
            #x.closeWorkbook()
    #x.closeWorkbook()
    d.closeConnection()


if __name__=='__main__':
    writeArticles()
