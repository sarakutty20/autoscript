#   Description:
#   CDS_BILL_BOM_CHECK.py
#   To send mail if any one of the least child is Make 
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    11/08/2016
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
from psdi.mbo import DBShortcut
from java.lang import System 
from java.rmi import RemoteException 
from java.sql import ResultSet
from java.util import Properties 
from javax.mail import Message 
from javax.mail import MessagingException 
from javax.mail import Session 
from javax.mail import Transport 
from javax.mail.internet import AddressException 
from javax.mail.internet import InternetAddress 
from javax.mail.internet import MimeMessage
from psdi.security import UserInfo 
from psdi.security import ConnectionKey 


import sys

v_custrefno = mbo.getString('CDS_CUSTOMER_REF_NO') 
v_wonum = mbo.getString('WONUM')
#Set Email Subject  			  
emailsub = "BOM does not exist for Quote Request Lines -  " + str(v_wonum)  
  
#Set Email Content 
  
emailcont = "Please find below  Quote Request Lines Customer reference no  : " + str(v_custrefno) 
  
#Set Email Address

v_emailid = "NO"
	
v_sender = "maxadmin@controlsdata.com"
v_cds_itemnum = mbo.getString("CDS_ITEMNUM")
v_whereclauseql = "exists ( select part_nbr from cds_part where part_type = 'M' and part_nbr = CDS_BILL.comp_part_nbr ) and CONNECT_BY_ISLEAF = 1 start with prnt_part_nbr = '"+str(v_cds_itemnum)+"' connect by PRIOR comp_part_nbr = prnt_part_nbr"
cdsbillmboset = mbo.getMboSet('$$CDSBOM','CDS_BILL',v_whereclauseql)
v_fulltable = []
v_leastchildren = []
recipientAddress = []
props = System.getProperties()
props.setProperty("mail.transport.protocol", "smtp")
v_mailhost = props.getProperty("mail.smtp.host")
props.setProperty("mail.host", v_mailhost)
v_isparticipated = False
if(cdsbillmboset.moveFirst() is not None):
	for i in range(0,cdsbillmboset.count()):
		cdsbillmbo = cdsbillmboset.getMbo(i)
		v_leastchild = cdsbillmbo.getString("COMP_PART_NBR")
		v_leastchildren.append(v_leastchild) 
		# print '******** Inside for rfqvendor **************************'		
	v_whereclauseemail = "personid in ( select RESPPARTYGROUP from PERSONGROUPTEAM where persongroup='MRP_CO')"
	emailmboset = mbo.getMboSet('$$EMAILLIST','EMAIL',v_whereclauseemail)
	if(emailmboset.moveFirst() is not None):
		v_isparticipated = True
		for j in range(0,emailmboset.count()):
			emailmbo = emailmboset.getMbo(j)
			v_email = emailmbo.getString("EMAILADDRESS")
			recipientAddress.append(InternetAddress(v_email))
			
	v_whereclausebom = "1=1 start with prnt_part_nbr = '"+str(v_cds_itemnum)+"' connect by PRIOR comp_part_nbr = prnt_part_nbr ORDER SIBLINGS BY comp_part_nbr"
	bommboset = mbo.getMboSet('$$CDSBOMSET','CDS_BILL',v_whereclausebom)
	mxServer = MXServer.getMXServer()
	conKey = mxServer.getSystemUserInfo().getConnectionKey()
	dbs = DBShortcut()
	dbs.connect(conKey)
	c = 0
	v_fulltable = []
	v_tablehdr = "<table border='1'><tr><th>Parent Part no </th><th>Comp Part no </th><th>Hierarchy Path </th></tr>"
	v_fulltable.append(v_tablehdr)	
	print "---Parent Part no------Comp Part no----------Remarks---------"
	try:
		rs = dbs.executeQuery("select PRNT_PART_NBR,COMP_PART_NBR,sys_connect_by_path(comp_part_nbr,'/') FULLPATH from CDS_BILL where 1=1 start with prnt_part_nbr = '"+str(v_cds_itemnum)+"' connect by PRIOR comp_part_nbr = prnt_part_nbr ORDER SIBLINGS BY comp_part_nbr")
		if("/" in v_cds_itemnum):
			v_cds_itemnum = "["+str(v_cds_itemnum)+"]"
		while(rs.next() and v_isparticipated ):
			v_parentpartnbr = rs.getString("PRNT_PART_NBR")
			v_comppartnbr 	= rs.getString("COMP_PART_NBR")
			v_fullpath		= rs.getString("FULLPATH")
			if("/" in v_parentpartnbr):
				v_parentpartnbr = "["+str(v_parentpartnbr)+"]"
			if("/" in v_comppartnbr):
				v_comppartnbr = "["+str(v_comppartnbr)+"]"
			v_tablecol1 = "<tr><td>"+str(v_parentpartnbr)+"</td>"
			v_tablecol2 = "<td>"+str(v_comppartnbr)+"</td>"
			v_tablecol3 = "<td>"+str(v_cds_itemnum)+str(v_fullpath)+"</td></tr>"
			if(v_comppartnbr in v_leastchildren):
				v_tablecol2 = "<td bgcolor='yellow'><font color='red'>"+str(v_comppartnbr)+"</font></td>"
				v_tablecol3 = "<td bgcolor='yellow'><font color='red'>"+str(v_cds_itemnum)+str(v_fullpath)+"</font></td></tr>"
			v_fulltable.append(v_tablecol1+v_tablecol2+v_tablecol3)
		v_fulltable.append("</table>")			
		rs.close()
		dbs.commit()
	except:
		print "Exception: ", sys.exc_info()
	finally:
		dbs.close()
	try:			
		session = Session.getDefaultInstance(props, None)
		message = MimeMessage(session)
		message.setContent("<h1>BOM Details </h1>", "text/html")
		message.setFrom(InternetAddress(v_sender))
		message.setSender(InternetAddress(v_sender))
		message.setSubject("BOM "+str(v_custrefno)+" details ")
		message.addRecipients(Message.RecipientType.TO,recipientAddress)
		message.setContent(''.join(v_fulltable), "text/html")														
		Transport.send(message)				
	except:
		print "In exception*******************"