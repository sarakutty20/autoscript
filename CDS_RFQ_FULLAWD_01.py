#   Description:
#   CDS_RFQ_FULLAWD_01.py
#   To send awarded and not awarded lines to Suppliers
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    25/11/2015
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                            N/A          S Ananthan
#
#    
#   Launch Point Variables
#   ----------------------
#                                         Action launch point
#
#   Relationships
#   -------------

from java.util import Calendar 
from java.util import Date 
from psdi.app.report import ReportUtil 
from psdi.server import MXServer 
from psdi.mbo import MboConstants 
from psdi.mbo import SqlFormat
from java.lang import System 
from java.rmi import RemoteException 
from java.util import Properties 
from javax.mail import Message 
from javax.mail import MessagingException 
from javax.mail import Session 
from javax.mail import Transport 
from javax.mail.internet import AddressException 
from javax.mail.internet import InternetAddress 
from javax.mail.internet import MimeMessage 


v_rfqnum = mbo.getString('RFQNUM') 
v_siteid = mbo.getString('SITEID')
#Set Email Subject  			  
emailsub = " Request for quotation   " + str(v_rfqnum)  
  
#Set Email Content 
  
emailcont = "Please find attached CDS Request for quotation : " + str(v_rfqnum) 
  
#Set Email Address

v_emailid = "NO"
	
v_sender = "maxadmin@controlsdata.com"
v_whereclauseql = "siteid = '"+str(v_siteid)+"' and rfqnum = '"+str(v_rfqnum)+"'"
rfqvendorSet = mbo.getMboSet('$$RFQV','RFQVENDOR',v_whereclauseql)
v_fulltable = []
props = System.getProperties()
props.setProperty("mail.transport.protocol", "smtp")
props.setProperty("mail.host", "172.24.24.120")
v_isparticipated = False
if(rfqvendorSet.moveFirst() is not None):
	for i in range(0,rfqvendorSet.count()):
		rfqvendormbo = rfqvendorSet.getMbo(i)
		# print '******** Inside for rfqvendor **************************'		
		if(rfqvendormbo is not None):
			v_emailid = rfqvendormbo.getString("EMAIL")
			v_vendor  = rfqvendormbo.getString("VENDOR")
			v_whereqline = "siteid = '"+str(v_siteid)+"' and rfqnum = '"+str(v_rfqnum)+"' and vendor = '"+str(v_vendor)+"'"
			rfqqtnlineSet = mbo.getMboSet('$$RFQQL','QUOTATIONLINE',v_whereqline)
			v_fulltable = []
			v_tablehdr = "<table><tr><th>RFQNUM</th><th>RFQLINENUM</th><th>VENDOR</th><th>ITEMNUM</th><th>ORDERQTY</th><th>ISAWARDED</th></tr>"
			print "---RFQ------RFQLINENUM----------VENDOR----------ITEMNUM-------QTY----------ISAWARDED"
			v_isparticipated = False
			v_fulltable.append(v_tablehdr) 
			if(rfqqtnlineSet.moveFirst() is not None):
				for j in range(0,rfqqtnlineSet.count()):
					v_isparticipated = True
					rfqqtnlinembo = rfqqtnlineSet.getMbo(j)					
					v_rfqlinenum = rfqqtnlinembo.getString("RFQLINENUM")
					v_itemnum = rfqqtnlinembo.getString("ITEMNUM")
					v_orderqty = rfqqtnlinembo.getString("ORDERQTY")
					v_isawarded = rfqqtnlinembo.getString("ISAWARDED")
					if(v_isawarded == "Y"):
					  v_isawarded = "YES"
					else:  
					  v_isawarded = "NO"	
					# print "---"+str(v_rfqnum)+"------"+str(v_rfqlinenum)+"----------"+str(v_vendor)+"----------"+str(v_itemnum)+"-------"+str(v_orderqty)+"----------"+str(v_isawarded)+""
					v_tablerow = "<tr><td>"+str(v_rfqnum)+"</td><td>"+str(v_rfqlinenum)+"</td><td>"+str(v_vendor)+"</td><td>"+str(v_itemnum)+"</td><td>"+str(v_orderqty)+"</td><td>"+str(v_isawarded)+"</td></tr>"
					v_fulltable.append(v_tablerow)	
		try:			
			session = Session.getDefaultInstance(props, None)
			message = MimeMessage(session)
			message.setContent("<h1>RFQ Details </h1>", "text/html")
			message.setFrom(InternetAddress(v_sender))
			message.setSender(InternetAddress(v_sender))
			message.setSubject("RFQ "+str(v_rfqnum)+" Awarded details ")
			message.addRecipient(Message.RecipientType.TO,InternetAddress(v_emailid))
			if(v_isparticipated == True):
				v_fulltable.append("</table>")
				# message.setText(''.join(v_fulltable))
				message.setContent(''.join(v_fulltable), "text/html")														
			if(v_isparticipated ==  False):
				v_fulltable = ["RFQ "+str(v_rfqnum)+" has been awarded to other vendor "]
				message.setContent(''.join(v_fulltable), "text/html")
			Transport.send(message)				
		except:
			print "In exception*******************"