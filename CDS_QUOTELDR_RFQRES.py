#   Description:
#   CDS_QUOTELDR_RFQRES.py
#   Create and send Quote response report to customer
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    08/12/2015
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

v_wonum = mbo.getString('WONUM') 
v_siteid = mbo.getString('SITEID')
v_orgid = mbo.getString('ORGID')
v_custrefno  = mbo.getString('CDS_CUSTOMER_REF_NO') 
v_cust  = mbo.getString('CDS_CUSTOMER') 
#Set Email Subject  			  
emailsub = " RFQ Response details for the reference " + str(v_custrefno)  
  
#Set Email Content 
  
emailcont = "Please find attached CDS RFQ Response : " + str(v_custrefno) 
  
#Set Email Address

v_emailid = "NO"
	
#Set Report Name 
v_reportname = "cds_worfqstdquote.rptdesign"
v_whereclauseql = " company = '"+str(v_cust)+"' and orgid = '"+str(v_orgid)+"'"
compcontSet = mbo.getMboSet('$$COMPC','COMPCONTACT',v_whereclauseql)
if(compcontSet.moveFirst() is not None):
		for i in range(0,compcontSet.count()):
		 compcontmbo = compcontSet.getMbo(i)
		 # print '********Inside for rfqvendor **************************'
		 if(compcontmbo is not None):
			v_emailid = compcontmbo.getString("EMAIL")			
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
							reportsched.setValue ("appname","WOTRACK_SO") 
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
																		cronparam.setValue("VALUE","wonum = '"+mbo.getString("WONUM")+"'",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   elif paramname=="paramdelimiter": 
																		print 'If condition for v_paramdelimiter'
																		cronparam.setValue("VALUE","|",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   elif paramname=="appname": 
																		cronparam.setValue("VALUE","WOTRACK_SO",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   elif paramname=="pwonum": 
																		cronparam.setValue("VALUE",mbo.getString("WONUM"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 
															   elif paramname=="psiteid": 
																		cronparam.setValue("VALUE",v_siteid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION) 		
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
							commlogmbo.setValue("OWNERTABLE","WORKORDER",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)	
							commlogmbo.setValue("MESSAGE","The email message sent by autoscript",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
							commlogmbo.setValue("OWNERID",mbo.getString("WORKORDERID"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)													
							reportschedset.save()