#   Description:
#   CDS_RFQ_01.py
#   Create and send RFQ report to supplier
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    17/11/2015
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

v_rfqnum = mbo.getString('RFQNUM') 
v_siteid = mbo.getString('SITEID')
#Set Email Subject  			  
emailsub = " Request for quotation   " + str(v_rfqnum)  
  
#Set Email Content 
  
emailcont = "Please find attached CDS Request for quotation : " + str(v_rfqnum) 
  
#Set Email Address

v_emailid = "NO"
	
#Set Report Name 
v_reportname = "cds_rfqprint.rptdesign"
v_whereclauseql = " CDS_RPTSENT = 0 and siteid = '"+str(v_siteid)+"' and rfqnum = '"+str(v_rfqnum)+"'"
rfqvendorSet = mbo.getMboSet('$$RFQV','RFQVENDOR',v_whereclauseql)
if(rfqvendorSet is not None):
		for i in range(0,rfqvendorSet.count()):
		 rfqvendormbo = rfqvendorSet.getMbo(i)
		 # print '********Inside for rfqvendor **************************'
		 if(rfqvendormbo is not None):
			v_emailid = rfqvendormbo.getString("EMAIL")
			v_vendor  = rfqvendormbo.getString("VENDOR")
			c = Calendar.getInstance() 
			# add 150 seconds to current time to allow preparing REPORTSCHED cron task instance 
			c.add(Calendar.SECOND,150) 
			d = c.getTime() 
			thisposet = mbo.getThisMboSet() 
			if thisposet is not None: 
					locale = thisposet.getClientLocale() 
					userinfo = thisposet.getUserInfo() 
					  
			schedule = ReportUtil.convertOnceToSchedule(d,locale,c.getTimeZone()) 
			print "Schedule we have to set into REPORTSCHED Cron task is: " + str(schedule) 
			if schedule is not None and v_emailid != "NO": 
					reportschedset = MXServer.getMXServer().getMboSet("REPORTSCHED",userinfo) 
					if reportschedset is not None: 
							print "Obtained REPORTSCHED set"
							reportsched = reportschedset.add() 
							reportsched.setValue("REPORTNAME",v_reportname) 
							reportsched.setValue ("appname","RFQ") 
							reportsched.setValue ("USERID","MAXADMIN") 
							reportsched.setValue ("TYPE","once") 
							reportsched.setValue("EMAILTYPE","attach") 
							reportsched.setValue("MAXIMOURL","http://172.24.24.116/maximo") 
							reportsched.setValue("EMAILUSERS",v_emailid) 
							reportsched.setValue("EMAILSUBJECT",emailsub) 
							reportsched.setValue("EMAILCOMMENTS",emailcont) 
							reportsched.setValue("EMAILFILETYPE","PDF") 
							reportsched.setValue("COUNTRY",locale.getCountry()) 
							reportsched.setValue("LANGUAGE",locale.getLanguage()) 
							reportsched.setValue("VARIANT",locale.getVariant()) 
							reportsched.setValue("TIMEZONE",thisposet.getClientTimeZone().getID()) 
							reportsched.setValue("LANGCODE","EN") 
							print "About to work with REPORTSCHEDULE cron task"
							crontaskdef = reportsched.getMboSet("$parent","crontaskdef","crontaskname='REPORTSCHEDULE'").getMbo(0) 
							if crontaskdef is not None: 
									crontaskinstset = crontaskdef.getMboSet("CRONTASKINSTANCE") 
									if crontaskinstset is not None: 
											 print "About to work with Cron task instance of REPORTSCHEDULE cron task"
											 crontaskinst = crontaskinstset.add(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
											 if crontaskinst is not None: 
													  d = Date() 
													  crontaskinstname = str(d.getTime()) 
													  crontaskinst.setValue("CRONTASKNAME","REPORTSCHEDULE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
													  crontaskinst.setValue("INSTANCENAME",crontaskinstname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
													  crontaskinst.setValue("SCHEDULE",schedule,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
													  crontaskinst.setValue("ACTIVE",1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
													  crontaskinst.setValue("RUNASUSERID",userinfo.getUserName(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
													  crontaskinst.setValue("HASLD",0,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
													  crontaskinst.setValue("AUTOREMOVAL",True,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
													  print "have set all cron task instance values for REPORTSCHEDULE cron task"
							reportsched.setValue("CRONTASKNAME",crontaskinst.getString("CRONTASKNAME")) 
							reportsched.setValue("INSTANCENAME",crontaskinst.getString("INSTANCENAME")) 
							print "Now going to work with Cron task PARAMETERS"
							cronparamset = crontaskinst.getMboSet("PARAMETER") 
							if cronparamset is not None: 
									 sqf = SqlFormat(cronparamset.getUserInfo(),"reportname=:1") 
									 sqf.setObject(1,"REPORTPARAM","REPORTNAME",v_reportname) 
									 reportparamset = MXServer.getMXServer().getMboSet("REPORTPARAM",cronparamset.getUserInfo()) 
									 if reportparamset is not None: 
											  print "working with REPORTPARAM mbo set"
											  reportparamset.setWhere(sqf.format()) 
											  reportparamset.reset() 
											  i=reportparamset.count() 
											  reportparammbo = None
											  for j in range(i): 
													   reportparam = reportparamset.getMbo(j) 
													   cronparam = cronparamset.add(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
													   if cronparam is not None: 
															   print "going to copy values from REPORTPARAM into CRONTASKPARAM"
															   cronparam.setValue("CRONTASKNAME","REPORTSCHEDULE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   cronparam.setValue("INSTANCENAME",crontaskinstname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   cronparam.setValue("CRONTASKNAME","REPORTSCHEDULE",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   paramname = reportparam.getString("PARAMNAME") 
															   cronparam.setValue("PARAMETER",paramname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   if paramname=="where": 
																		# prepare dynamic where clause for report params 
																		uniqueidname = mbo.getUniqueIDName() 
																		uniqueidvalue = mbo.getUniqueIDValue() 
																		uniquewhere = uniqueidname + "=" + str(uniqueidvalue) 
																		cronparam.setValue("VALUE",uniquewhere,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   elif paramname=="paramstring": 
																		print 'If condition for v_paramstring'
																		cronparam.setValue("VALUE","rfqnum = '"+mbo.getString("RFQNUM")+"'",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   elif paramname=="paramdelimiter": 
																		print 'If condition for v_paramdelimiter'
																		cronparam.setValue("VALUE","|",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   elif paramname=="appname": 
																		cronparam.setValue("VALUE","RFQ",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   elif paramname=="pRfqnum": 
																		cronparam.setValue("VALUE",mbo.getString("RFQNUM"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   elif paramname=="pCompany": 
																		cronparam.setValue("VALUE",v_vendor,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 		
															   else: 
																		continue
							commlogset = mbo.getMboSet("COMMLOG")
							commlogmbo = commlogset.add(MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
							#commlogmbo.setValue("ORGAPP","AUTOSCRIPT")
							commlogmbo.setValue("SENDTO",v_emailid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
							commlogmbo.setValue("SENDFROM","maxadmin@test.controlsdata.com",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)							
							commlogmbo.setValue("SUBJECT","email subject sent by the autoscript",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
							commlogmbo.setValue("CREATEBY","MAXADMIN",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)	
							commlogmbo.setValue("CREATEDATE",Date(),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)	
							commlogmbo.setValue("OWNERTABLE","RFQ",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)	
							commlogmbo.setValue("MESSAGE","The email message sent by autoscript",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
							commlogmbo.setValue("OWNERID",mbo.getString("RFQID"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)													
							reportschedset.save()
			rfqvendormbo.setValue("CDS_RPTSENT",1)