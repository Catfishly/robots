#!/usr/bin/python
#coding:utf-8

'''save data from qiubai.py to MYSQL test/qiubai'''

'''
articleID
print 'author:',find.group('author').strip()
print 'content:',find.group('content').strip()
print 'stats-vote:',find.group('stats_vote').strip()
print 'stats-comments:',find.group('stats_comments').strip()

'''
import MySQLdb as mydb

def setDelimiter(name='-'):
    lengh=40
    half=(lengh-len(name))/2
    print '-'*half+name+'-'*half

def setQiubaiDb(cursor):
    setDelimiter('init qiubai database')
    setDbSql='''
    CREATE TABLE IF NOT EXISTS qiubai(
    articleID CHAR(20) UNIQUE NOT NULL PRIMARY KEY,
    author VARCHAR(20),
    content VARCHAR(300),
    stats_vote INT,
    stats_comments INT
    ) ENGINE=INNODB DEFAULT CHARSET=UTF8
    '''
    cursor.execute(setDbSql)

def getQiubaiDb(password='-'):
    setDelimiter('try database connect')
    userName='root'
    hostName='114.215.108.67'
    dbName='test'
    portName=3306
    try:
        conn=mydb.connect(host=hostName,user=userName,passwd=password,db=dbName,port=portName)
    except mydb.OperationalError:
        while True:
            password=raw_input('password for %s:'%userName)
            try:
                conn=mydb.connect(host=hostName,user=userName,passwd=password,db=dbName,port=portName)
                break
            except mydb.OperationalError:
                continue
    curs=conn.cursor()
    searchDbSql='SELECT * FROM qiubai'
    try:
        curs.execute(searchDbSql)
    except:
        setDelimiter('no DB qiubai found')
        setQiubaiDb(curs)
    setDelimiter('database well connect')
    return (conn,curs)
if __name__=='__main__':
    getQiubaiDb()
