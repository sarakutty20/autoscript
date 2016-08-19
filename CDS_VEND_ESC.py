#   Description:
#   CDS_VEND_ESC.py
#   Insert/Update into COMPANIES after inserting/updating into CDS_VEND 
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    13/07/2016
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                            N/A         S Ananthan
#  
#    
#   Launch Point Variables
#   ----------------------
#   Object launch point Add and Update
#
#   Relationships
#   -------------

from java.util import Calendar 
from java.util import Date 
from psdi.server import MXServer 
from psdi.mbo import MboConstants 
from psdi.mbo import SqlFormat


def translog(v_key,v_status,v_tablename,v_errormsg):
	#print "==============In Trans Log v_key ========="+str(v_key)
	#print "==============In Trans Log v_errormsg===== "+str(v_errormsg)
	cdstranslogset = MXServer.getMXServer().getMboSet("CDS_TRANS_LOG", mbo.getUserInfo())
	cdstranslogmbo = cdstranslogset.add()
	cdstranslogmbo.setValue("KEY",v_key,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogmbo.setValue("TABLENAME",v_tablename,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogmbo.setValue("TRANSDATE",v_date,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogmbo.setValue("ERRORMSG",v_errormsg,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogmbo.setValue("STATUS",v_status,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	mbo.setValue("PROCESSED",True,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogset.save()
	return
	
def addcompany(compnyset,v_company,v_name,v_currency_code,v_type):
	print "======Add company ===v_compay========="+str(v_company)
	companymbo = compnyset.add()	
	companymbo.setValue("COMPANY",v_company,MboConstants.SAMEVALUEVALIDATION)
	companymbo.setValue("NAME",v_name,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	companymbo.setValue("CURRENCYCODE",v_currency_code,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	companymbo.setValue("TYPE",v_type,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	companymbo.setValue("ORGID",v_orgid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	compnyset.save()
	return	

v_processed_status	= "PROCESSED"
v_error_status		= "ERROR"
v_custtype	 		= "CUST"
v_vendtype 			= "VEND"
v_orgid 			= "RRCDS"
v_custandvend		= "C&V"

v_tablename 		= mbo.getName()
v_key 				= mbo.getString(str(v_tablename)+"ID") 
print "===========v_tablename==========="+str(v_tablename)
print "===========v_key==========="+str(v_key)
v_date 				= MXServer.getMXServer().getDate()

if(v_tablename == "CDS_VEND"):
	v_vendor_id = mbo.getString("VENDOR_ID")
	v_vendor_name = mbo.getString("VENDOR_NAME")
	v_currency_cd = mbo.getString("CURRENCY_CODE")
	print "===========Processing CDS_VEND data ========="
	v_whereclausecomp = "company = '"+str(v_vendor_id)+"'"
	compset = mbo.getMboSet('$$VENDCOMPANIES','COMPANIES',v_whereclausecomp)
	if(compset.moveFirst() is not None):
		print "===========Processing CDS_VEND data Inside if ========="
		compmbo = compset.getMbo(0)
		v_comptype = compmbo.getString("TYPE")
		if(v_comptype == v_custtype):
			v_comptype = v_custandvend
			compmbo.setValue("TYPE",v_comptype,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		compmbo.setValue("NAME",v_vendor_name,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		compmbo.setValue("CURRENCYCODE",v_currency_cd,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		translog(v_key,v_processed_status,v_tablename,"")
	else:
		print "===========Processing CDS_VEND data Inside else ========="
		addcompany(compset,v_vendor_id,v_vendor_name,v_currency_cd,v_vendtype)
		translog(v_key,v_processed_status,v_tablename,"")