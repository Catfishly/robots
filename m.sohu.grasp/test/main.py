#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

'''
import sys,os
from optparse import OptionParser
import grasp
import time
def main():
	usage="python %prog [options] args"
	parser=OptionParser(usage)
	parser.add_option('-d','--delayTime',help='time to be waited',dest='delayTime')
	parser.add_option('-o','--oo',help='dir to save files',dest='dir')
	parser.add_option('-u','--url',help='url',dest='url')
	(options,args)=parser.parse_args()
	#if len(args)!=1:
	#	parser.error('incorrecter of arguments')
	while True:
		if not os.path.isdir(options.dir):
			os.makedirs(options.dir)
		#corrent_dir=os.getcwd()
		os.chdir(options.dir)
		sub_dir=time.strftime('%Y%m%d%H%M%S',time.localtime())
		os.mkdir(sub_dir)
		os.chdir(sub_dir)
		grasp.getContent(options.url)
		os.chdir(options.dir)	
		print 'saved'
		time.sleep(int(options.delayTime))
		

if __name__=='__main__':
	#    pass
	main()
