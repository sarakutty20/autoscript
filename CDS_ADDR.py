#   Description:
#   CDS_ADDR.py
#   Insert/Update into COMPANIES and COMPCONTACT after inserting/updating into CDS_ADDR 
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    14/07/2016
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
	cdstranslogset = MXServer.getMXServer().getMboSet("CDS_TRANS_LOG", mbo.getUserInfo())
	cdstranslogmbo = cdstranslogset.add()
	cdstranslogmbo.setValue("KEY",v_key,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogmbo.setValue("TABLENAME",v_tablename,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogmbo.setValue("TRANSDATE",v_date,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogmbo.setValue("ERRORMSG",v_errormsg,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogmbo.setValue("STATUS",v_status,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdstranslogset.save()
	return

def addcompcontact(compcontset,v_contname,v_emailid,v_contphone,v_type):
	compcontmbo = compcontset.add()
	compcontmbo.setValue("CONTACT",v_contname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	compcontmbo.setValue("EMAIL",v_emailid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	compcontmbo.setValue("VOICEPHONE",v_contphone,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	compcontmbo.setValue("CDS_CONTACTTYPE",v_type,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	compcontset.save()
	return	
	
v_tablename_cds_addr = "CDS_ADDR"
v_processed_status	= "PROCESSED"
v_error_status		= "ERROR"
v_custtype	 		= "CUST"
v_vendtype 			= "VEND"
v_orgid 			= "RRCDS"
v_error_msg			= "Customer Id or Vendor id does not exist"

v_tablename 		= mbo.getName()
v_key 				= mbo.getString(str(v_tablename)+"ID") 
print "===========v_tablename==========="+str(v_tablename)
print "===========v_key==========="+str(v_key)
v_date 				= MXServer.getMXServer().getDate()

if(v_tablename == "CDS_ADDR"):
	v_cust_id 		= mbo.getString("CUST_ID")
	v_frmt_ln_1 	= mbo.getString("FREE_FRMT_LN_1")
	v_frmt_ln_2 	= mbo.getString("FREE_FRMT_LN_2")
	v_frmt_ln_3 	= mbo.getString("FREE_FRMT_LN_3")
	v_frmt_ln_4 	= mbo.getString("FREE_FRMT_LN_4")
	v_frmt_ln_5 	= mbo.getString("FREE_FRMT_LN_5")
	v_postcode 		= mbo.getString("POSTAL_CD")
	v_countrycode 	= mbo.getString("COUNTRY_CD")
	v_attnln 		= mbo.getString("ATTN_LN")
	v_deliverypoint = mbo.getString("DELIVERY_POINT")
	v_contactname 	= mbo.getString("CONTCT_NAME")
	v_contactphone 	= mbo.getString("CONTCT_PHONE")
	v_email1 		= mbo.getString("USER_FLD_1")
	v_email2 		= mbo.getString("USER_FLD_2")
	v_cds_attention = '-'.join(filter(None, (v_attnln, v_deliverypoint)))
	v_email = ','.join(filter(None, (v_email1, v_email2)))
	v_frmt_ln_merge1 = ','.join(filter(None, (v_frmt_ln_3, v_frmt_ln_4,v_frmt_ln_5)))
	v_frmt_ln_merge2 = ','.join(filter(None, (v_frmt_ln_4,v_frmt_ln_5)))
	
	print "===========Processing CDS_CUST data ========="
	v_whereclausecomp = "company = '"+str(v_cust_id)+"'"
	v_whereclausecomp1 = "and type in ('CUST','C&V')"
	v_whereclausecompcontact = "company = '"+str(v_cust_id)+"' and contact = '"+str(v_contactname)+"'"
	compset = mbo.getMboSet('$$CUSTCOMPANIES','COMPANIES',v_whereclausecomp+v_whereclausecomp1)
	compcontactset = mbo.getMboSet('$$COMPCONTACT','COMPCONTACT',v_whereclausecomp)
	compcontactaddset = mbo.getMboSet('$$COMPCONTACTEXIST','COMPCONTACT',v_whereclausecompcontact)
	if(not compset.isEmpty()):
		compcontactset.setOwner(compset.getMbo(0))
		if(compcontactset.moveFirst() is not None):
			#for loop and update 
			for j in range(0,compcontactset.count()):					
				compcontactmbo 	= compcontactset.getMbo(j)
				v_compcontactname = compcontactmbo.getString("CONTACT")
				if(v_compcontactname == v_contactname):
					compcontactmbo.setValue("EMAIL",v_email,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
					compcontactmbo.setValue("VOICEPHONE",v_contactphone,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
					compcontactmbo.setValue("CDS_CONTACTTYPE",v_custtype,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
			if(compcontactaddset.isEmpty()):
				# add to compcontact 
				addcompcontact(compcontactset,v_contactname,v_email,v_contactphone,v_custtype)
		else:
			# add to compcontact 
			addcompcontact(compcontactset,v_contactname,v_email,v_contactphone,v_custtype)
	if(compset.moveFirst() is not None):
		print "===========Processing CDS_CUST data Inside if ========="
		compmbo = compset.getMbo(0)
		v_name = compmbo.getString("NAME")
		v_contact = compmbo.getString("CONTACT")
		compmbo.setValue("CDS_ATTENTION",v_cds_attention,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		compmbo.setValue("ADDRESS4",v_postcode,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		compmbo.setValue("CDS_COUNTRY",v_countrycode,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		compmbo.setValue("CONTACT",v_contactname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		#if(v_contact == ""): 
		#	compmbo.setValue("CONTACT",v_contactname,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		print "===========Processing CDS_CUST data Inside if v_name========="+str(v_name)
		print "===========Processing CDS_CUST data Inside if v_frmt_ln_1========="+str(v_frmt_ln_1)
		if(v_name == v_frmt_ln_1):
			print "===========******Processing CDS_CUST data Inside second ifffff "
			compmbo.setValue("ADDRESS1",v_frmt_ln_2,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
			compmbo.setValue("ADDRESS2",v_frmt_ln_3,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
			compmbo.setValue("ADDRESS3",v_frmt_ln_merge2,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		else:
			print "===========******Processing CDS_CUST data Inside second else "
			compmbo.setValue("ADDRESS1",v_frmt_ln_1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
			compmbo.setValue("ADDRESS2",v_frmt_ln_2,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
			compmbo.setValue("ADDRESS3",v_frmt_ln_merge1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		compset.save()
		translog(v_key,v_processed_status,v_tablename_cds_addr,"")
	else:
		translog(v_key,v_error_status,v_tablename_cds_addr,v_error_msg)