#!/usr/local/Python-2.7.3/bin/python
import sys
import MySQLdb
import cgi
import cgitb
import re
import datetime, os, string
cgitb.enable()

def htmlImageFolder():
        return '/www/html/students_13/gawa/'

def image_timeout():
	return 24*60*60*100000 #24 hours in deciseconds

def zip_timeout():
	return 24*60*60*100000 #24 hours in deciseconds

def createAnimatedGIF(strArr):
	if (not isinstance(strArr,list)):
		print "Input is not an array"
		return None
	if len(strArr)<1:
		print "Array cannot be empty"
		return []

	from PIL import Image
	from images2gif import writeGif

	resultArr = convertToGIF(strArr,700,fullPath=False)

	images = [Image.open(fn) for fn in resultArr]
	tempfolder = os.path.split(resultArr[0])[0]
	epochtime = str(datetime.datetime.now().strftime('%s%f'))
	dstPath = os.path.join(tempfolder,"my_gif"+epochtime+".GIF")
	output = writeGif(dstPath,images, duration=0.2)

	if(os.path.exists(dstPath)):
		return [getURLPath(dstPath)]
	else:
		print "I failed to create animated GIF "+filename
		return None

def convertToGIF(strArr,size=-1,fullPath=True):
	if (not isinstance(strArr,list)):
		print "Input is not an array"
		return None
	if len(strArr)<1:
		print "Array cannot be empty"
		return []

	import shutil
	from subprocess import call
	
	epochtime = str(datetime.datetime.now().strftime('%s%f'))
	tempfolder = os.path.join(htmlImageFolder(),"anigif",epochtime) 

	if not os.path.exists(tempfolder):os.makedirs(tempfolder)
	resultArr = []
	
	#This section removes all th directories created that are older than 6 minutes.
	for top, dirs, files in os.walk(os.path.dirname(tempfolder)):
	    for subd in dirs:
		if subd.isdigit(): 
			tstamp = int(subd)
			if int(datetime.datetime.now().strftime('%s%f'))-tstamp>image_timeout():
                                try :
                                        shutil.rmtree(os.path.join(top,subd))
                                except :
                                        pass


	for fiPath in strArr:
		if fiPath.endswith('.tif'):
			
			justName = os.path.split(fiPath)[-1].split('.')[0]
			dstPath = os.path.join(tempfolder,justName + ".gif")
			if os.path.exists(dstPath):os.remove(dstPath)			
			if(size is None or not isinstance(size,int) or size < 0):
				output = call(["/usr/bin/convert",fiPath, dstPath])
			else:
				output = call(["/usr/bin/convert","-resize",str(size)+"x"+str(size),fiPath, dstPath])

			if(os.path.exists(dstPath)):
				if(fullPath): dstPath = getURLPath(dstPath)
				resultArr.append(dstPath)

	return resultArr

def convertToThumb(strArr,fullPath=True):
	return convertToGIF(strArr,size=200,fullPath=fullPath)

def copyTifFile(strArr):
	from shutil import copyfile
	output = []
	epochtime = str(datetime.datetime.now().strftime('%s%f'))
	tempfolder = os.path.join(htmlImageFolder(),"anigif",epochtime)
        if not os.path.exists(tempfolder):os.makedirs(tempfolder)

	for fi in strArr:
		dest = os.path.join(tempfolder,os.path.split(fi)[-1])
		copyfile(fi, dest)
		if not os.path.exists(dest):
			print "I didn't copy the file correctly"
		output.append(getURLPath(dest))
	return output

def zipImages(sourceFolder):
	import zipfile
	epochtime = str(datetime.datetime.now().strftime('%s%f'))
	dfolder = os.path.join(htmlImageFolder(),'zips')
	if not os.path.exists(dfolder):os.makedirs(dfolder)
	dfile = os.path.join(dfolder,epochtime+".zip")
	zf = zipfile.ZipFile(dfile, "w")
	containFolder = os.path.abspath(sourceFolder)
	for dirname, subdirs, files in os.walk(containFolder):
	        for filename in files:
			filepath = os.path.abspath(os.path.join(dirname, filename))
			zf.write(filepath, filename)
	zf.close()

	#This section removes all the files created that are older than 2 minutes.
        for top, dirs, files in os.walk(dfolder):
            for file in files:
		fname = file.split('.')[0]
                if fname.isdigit():
                        tstamp = int(fname)
                        if int(datetime.datetime.now().strftime('%s%f'))-tstamp>zip_timeout():
                                try :
					os.remove(os.path.join(top,file))
				except :
					pass
	return getURLPath(dfile)



def print_to_file(strArr):
        import os,datetime
        epochtime = str(datetime.datetime.now().strftime('%s%f'))
        dfolder = os.path.join( htmlImageFolder(),'images')
        if not os.path.exists(dfolder):os.makedirs(dfolder)

        txtfile = os.path.join(dfolder,epochtime+".txt")
        text_file = open(txtfile, "w")
        for filepath in strArr:
                text_file.write(filepath+'\n')
        text_file.close()


        #Remove old text fiels
        for dirname, subdirs, files in os.walk(dfolder):
                for filename in files:
                        filename = filename.split('.')[0]
                        if filename.isdigit():
                                tstamp = int(filename)
                                if int(datetime.datetime.now().strftime('%s%f'))-tstamp>image_timeout():
                                        try :
                                                os.remove(os.path.join(dirname,filename))
                                        except :
                                                pass

        if(os.path.exists(txtfile)):
                return getURLPath(txtfile)
        return None


def getURLPath(path):
	str1 = path.split('html/')[-1]
	httpAdr = "http://bioed.bu.edu/"
	dstPath = httpAdr+str1
	return dstPath
