#   Description:
#   CDS_RFQ_AWD_CAN_01.py
#   Creation of RFQ and RFQ lines for a Quote Request Line
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
from psdi.mbo import MboSetEnumeration  



v_rfqnum = mbo.getString('RFQNUM') 
v_siteid = mbo.getString('SITEID')
#Set Email Subject  			  
emailsub = " Request for quotation   " + str(v_rfqnum)  
  
#Set Email Content 
  
emailcont = "Please find attached CDS Request for quotation : " + str(v_rfqnum) 
  
#Set Email Address

v_emailid = "NO"
props = System.getProperties()
props.setProperty("mail.transport.protocol", "smtp")
v_mailhost = props.getProperty("mail.smtp.host")
props.setProperty("mail.host", v_mailhost)
session = Session.getDefaultInstance(props, None)
v_sender = "maxadmin@controlsdata.com"
v_whereclauseql = "siteid = '"+str(v_siteid)+"' and rfqnum = '"+str(v_rfqnum)+"'"
rfqvendorSet = mbo.getMboSet('$$RFQV','RFQVENDOR',v_whereclauseql)
rfqvendorsetenum  = MboSetEnumeration(rfqvendorSet)
while (rfqvendorsetenum.hasMoreElements()):
	rfqvendormbo = rfqvendorsetenum.nextMbo()
	if(rfqvendormbo is not None):
		v_emailid = rfqvendormbo.getString("EMAIL")
		v_vendor  = rfqvendormbo.getString("VENDOR")
		message = MimeMessage(session)	
		try:
			message.setContent("<h1>RFQ Cancel</h1>", "text/html")
			message.setFrom(InternetAddress(v_sender))
			message.setSender(InternetAddress(v_sender))
			message.setSubject("RFQ "+str(v_rfqnum)+" Cancelled ")
			message.setText("We are sorry to inform you that the RFQ "+str(v_rfqnum)+" has been cancelled ")
			message.addRecipient(Message.RecipientType.TO,InternetAddress(v_emailid))
			Transport.send(message)
		except:
			print "In exception*******************"