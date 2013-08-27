#!/usr/local/Python-2.7.3/bin/python
import sys
import MySQLdb
import cgi
import cgitb
import re
cgitb.enable()

def printXHTMLHeader():
	print"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" >"""



def printROIHeader():
	printXHTMLHeader()

	print """
	<head>
	<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8" />
	<title> Testing Stuff </title>
	<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
	<link rel="stylesheet" type="text/css" href="/students_13/gawa/style_new.css" />
	<script>
	$(document).ready(function(){
		function scrollList(element){
			var rowpos = $("#RIOTable #"+element).position();
			var scrollTop = $("#RIOTable").scrollTop();
			var scrollBottom  = scrollTop + $("#RIOTable").height();
			var itembottom = rowpos.top + $("#RIOTable #"+element).height();
			if(rowpos.top<scrollTop || itembottom >=scrollBottom){
				$("#RIOTable").scrollTop(rowpos.top);
			}
		}
		function scrollImage(element){
			var el = $("#ROIimage #"+element);
			var scrl = $("#ROIimage");

			var rowpos = el.position();
			var scrollTop = scrl.scrollTop();
			var scrollBottom  = scrollTop + scrl.height();
			var itembottom = rowpos.top + el.height();

			if(rowpos.top<scrollTop || itembottom >=scrollBottom){
				scrl.scrollTop(rowpos.top);
			}

			var scrollLeft = scrl.scrollLeft();
			var scrollRight  = scrollLeft + scrl.width();
			var itemright = rowpos.left + el.width();

			if(rowpos.left<scrollLeft || itemright >=scrollRight){
				scrl.scrollLeft(scrollLeft + rowpos.left);
			}

		}
	
                function highlightTableElement(element) {
                        $("#RIOTable #"+element).css('background', '#C1A3A5');
			$("#ROIimage a#"+element).addClass('mouseover');
                }

                function clearTableElement(element) {
                        $("#RIOTable #"+element).css('background', '#FFFFFF');
			$("#ROIimage a#"+element).removeClass('mouseover')
                }

		function printLink(element){
			var hlink = $("#ROIimage a#"+element+" span").attr('id');
			$('#RIOTable .selected').removeClass('selected');
			$('#RIOTable #'+element+" td").addClass('selected');
			$('#ROIimage .selected').removeClass('selected');
			$('#ROIimage a#'+element).addClass('selected');
			var infoSection = $("#ROIinformation span");
			infoSection.html("");
			infoSection.append(hlink);
		}

		$("#ROIimage a").bind("mouseover", function() {highlightTableElement($(this).attr('id'));});
		$("#ROIimage a").bind("mouseout", function() {clearTableElement($(this).attr('id'));});
		$("#RIOTable .listItem").bind("mouseover", function() {highlightTableElement($(this).attr('id'));});
		$("#RIOTable .listItem").bind("mouseout", function() {clearTableElement($(this).attr('id'));});
		$("#RIOTable .listItem").bind("click", function(){
			var elID = $(this).attr('id');
			printLink(elID);
			scrollImage(elID);
		});
		$("#ROIimage a").bind("click", function() {
			var elID = $(this).attr('id');
			printLink(elID);
			scrollList(elID);
		});
	});

	</script>
	</head>
	"""

def printBody(imagePath,ROIDict,ROIProp):
	imageLink,listLink = getROIHtml(ROIDict)

	print """
	<body>
	<div id="content_wrapper_inner">
	<div id="ROIPage_wrapper_outer">
	<div id="ROIPageTitle" >
	
	<h1>Specific ROI Title</h1>
	</div>"""
	printROITable(listLink)
	print"""
	<div>
	<div id="ROIimage">
	<img src="%s" alt="Regions Of Interest Image">
	
	"""%(imagePath)
	
	print imageLink
	print "</div></div>"

	printROIinfoSection(ROIProp)
	print """</div></div></body>"""
	print """</html>"""

def getROIHtml(ROIDict):
	imageLink =""
	tablerows =""

	for item in ROIDict:
		someID = item['ID']
		xpos = str(item['xpos'])
		ypos = str(item['ypos'])
		dx = str(item['dx'])
		dy = str(item['dy'])
		identifier = item['identifier']

		imageLink += """
		<a id="%s" title="Region %s" style="left:%spx;top:%spx;height:%spx;width:%spx;">
		<span id="ROI #%s (%s,%s)"/>
		</a>"""%(someID,identifier,xpos,ypos,dx,dy,identifier,xpos,ypos)

		tablerows+="""
		<tr class="listItem" id="%s">
		<td><a><span>Region %s</span></a></td>
		</tr> """ %(someID,identifier)

	return imageLink,tablerows

def printROITable(tablerows):
	print """
	<div id="RIOTable">
	<table cellspacing="0" cellpadding="1" border="1">
	"""
	print tablerows
	
	print """
	</table>
	</div>"""

def printROIinfoSection(ROIProp):
	print """
	<div id="ROIinformation">
	<h2><span id="name">ROI Information:</span></h2>"""
	
        print '<table border="0">'
        for key in ROIProp:
                print '<tr><td><b>%s: </b></td><td>%s</td></tr>'%(key,ROIProp[key])
        print'</table>'

	print "	</div>"


def connect_db(db,username,pswd):
        #connect to database
        connection = MySQLdb.connect (host="localhost", db=db, user=username, passwd=pswd)
        #get cursor
        cursor = connection.cursor()
        return cursor, connection

def close_db(cursor, connection):
        #close cursor and connection
        try:
                cursor.close()
                connection.close()
        except:
                print "There was an error closing the connection."

def run_query(cursor, query):
        try:
                cursor.execute(query)
                desc = cursor.description
        except:
                print "There was an error running your script.\n"
                print "Please check your script and try again. \n"
                sys.exit(1)

        results = cursor.fetchall()
        return results



username = 'amauche'
password = 'amauche'
cursor, connection = connect_db("gawa",username,password)

exp = '20120105T143838'
rois = '20120118T163520'
iid = '62982'
RoiProps = {'Experiment ID':exp,'ROI Serial':rois,'Image ID':iid}

query1 = "select distinct x,y,dx,dy,imageFilename from (Image natural join (Image_has_ROI natural join ROI)) where experiment_eid= '%s' and ROISerial='%s' and iid=%s group by x,y;"%(RoiProps['Experiment ID'],RoiProps['ROI Serial'],RoiProps['Image ID'])
ans = run_query(cursor,query1)

path = ans[0][4]
#print path
import GawaImage
images = GawaImage.convertToGIF([path])
ImagePath = images[0]

ROIDict=[]
for i in range(len(ans)):
	ROIDict.append({'ID':"paul"+str(i),'xpos':ans[i][0],'ypos':ans[i][1],'dx':ans[i][2],'dy':ans[i][3],'identifier':str(i+1)})


printROIHeader()
printBody(ImagePath,ROIDict,RoiProps)


close_db(cursor, connection)
