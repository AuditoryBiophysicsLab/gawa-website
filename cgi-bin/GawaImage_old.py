#!/usr/local/Python-2.7.3/bin/python
import sys
import MySQLdb
import cgi
import cgitb
import re
cgitb.enable()

def createAnimatedGIF(strArr):
        if (not isinstance(strArr,list)):
                print "Input is not an array"
                return None
        if len(strArr)<1:
                print "Array cannot be empty"
                return []

        from PIL import Image
        from images2gif import writeGif
        import os, datetime

        resultArr = convertToGIF(strArr,700,fullPath=False)

        images = [Image.open(fn) for fn in resultArr]
        tempfolder = os.path.split(resultArr[0])[0]
        epochtime = str(datetime.datetime.now().strftime('%s'))
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

        import os, tempfile, datetime,shutil
        from subprocess import call

        epochtime = str(datetime.datetime.now().strftime('%s'))
        mystuff = '/www/html/students_13/amauche'
        tempfolder = os.path.join(mystuff,"images",epochtime)

        if not os.path.exists(tempfolder):os.makedirs(tempfolder)
        resultArr = []

        #This section removes all th directories created that are older than 6 minutes.
        for top, dirs, files in os.walk(os.path.dirname(tempfolder)):
            for subd in dirs:
                if subd.isdigit():
                        tstamp = int(subd)
                        if int(datetime.datetime.now().strftime('%s'))-tstamp>360:
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


def zipImages(sourceFolder):
        import os,datetime,zipfile
		
        destination='/www/html/students_13/amauche'
        epochtime = str(datetime.datetime.now().strftime('%s'))
		
        dfolder = os.path.join(destination,'zipfiles')
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
                        if int(datetime.datetime.now().strftime('%s'))-tstamp>120:
                                try :
                                        os.remove(os.path.join(top,file))
                                except :
                                        pass
        return getURLPath(dfile)



def getURLPath(path):
        str1 = path.split('html/')[-1]
        httpAdr = "http://bioed.bu.edu/"
        dstPath = httpAdr+str1
        return dstPath

