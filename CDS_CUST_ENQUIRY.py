#   Description:
#   CDS_CUST_ENQUIRY.py
#   Insert into WORKORDER and CDS_ORD_ITEM after inserting into CDS_CUST_ENQUIRY 
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    21/07/2016
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
from psdi.server import MaxVarServiceRemote
from psdi.server import MaxVars


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

def addwo(wombo,v_part_no,v_date_requested,v_quote_validity,v_quote_desc,v_quote_qty_1,v_quote_qty_2,v_quote_qty_3,v_quote_qty_4,
			v_quote_price_1,v_quote_price_2,v_quote_price_3,v_quote_price_4,v_quote_price_lt_1,v_quote_price_lt_2,v_quote_price_lt_3,v_quote_price_lt_4):
	wombo.setValue("CDS_ITEMNUM",v_part_no)
	wombo.setValue("CDS_QUOTE_VALIDITY",v_quote_validity)
	wombo.setValue("REQ_QTY_1",v_quote_qty_1)
	wombo.setValue("REQ_QTY_2",v_quote_qty_2)
	wombo.setValue("REQ_QTY_3",v_quote_qty_3)
	wombo.setValue("REQ_QTY_4",v_quote_qty_4)
	wombo.setValue("CDS_COST_NET_QTY_1",v_quote_price_1)
	wombo.setValue("CDS_COST_NET_QTY_2",v_quote_price_2)
	wombo.setValue("CDS_COST_NET_QTY_3",v_quote_price_3)
	wombo.setValue("CDS_COST_NET_QTY_4",v_quote_price_4)
	wombo.setValue("CDS_LEADTIME_QTY_1",v_quote_price_lt_1)
	wombo.setValue("CDS_LEADTIME_QTY_2",v_quote_price_lt_2)
	wombo.setValue("CDS_LEADTIME_QTY_3",v_quote_price_lt_3)
	wombo.setValue("CDS_LEADTIME_QTY_4",v_quote_price_lt_4)
	wombo.setValue("CHANGEBY","MAXADMIN")
	wombo.setValue("DESCRIPTION",v_quote_desc)
	wombo.setValue("NEWCHILDCLASS","WORKORDER")
	wombo.setValue("ORGID","RRCDS")
	wombo.setValue("REPORTEDBY","MAXADMIN")
	wombo.setValue("WORKTYPE","OTASK")
	wombo.setValue("CDS_OP_TYPE","ORDITEM")
	wombo.setValue("STATUS","HISTORIC",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("WOACCEPTSCHARGES","1")
	wombo.setValue("WOCLASS","WORKORDER")
	wombo.setValue("WOSEQUENCE","1",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("CDS_HISTORIC","1",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ACTINTLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ACTINTLABHRS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ACTLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ACTLABHRS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ACTMATCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ACTOUTLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ACTOUTLABHRS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ACTSERVCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ACTTOOLCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("AMS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("AOS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("APPTREQUIRED","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("CDS_CHILDCOMP","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("CHARGESTORE","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("DISABLED","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("DOWNTIME","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTATAPPRINTLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTATAPPRINTLABHRS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTATAPPRLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTATAPPRLABHRS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTATAPPRMATCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTATAPPROUTLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTATAPPROUTLABHRS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTATAPPRSERVCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTATAPPRTOOLCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTDUR","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTINTLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTINTLABHRS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTLABHRS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTMATCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTOUTLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTOUTLABHRS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTSERVCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ESTTOOLCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("FLOWACTIONASSIST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("FLOWCONTROLLED","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("HASCHILDREN","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("HASFOLLOWUPWORK","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("HISTORYFLAG","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("IGNOREDIAVAIL","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("IGNORESRMAVAIL","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("INCTASKSINSCHED","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("INTERRUPTIBLE","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("ISTASK","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("LMS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("LOS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("NESTEDJPINPROCESS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("OUTLABCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("OUTMATCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("OUTTOOLCOST","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("PARENTCHGSSTATUS","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("PLUSCISMOBILE","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("PLUSCLOOP","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("REQASSTDWNTIME","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("STATUSIFACE","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("SUSPENDFLOW","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("WOISSWAP","0",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("CDS_HLEVEL","1",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("CDS_HLEVEL_STR","-1",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	wombo.setValue("CDS_ITEMSETID","ITEMSET",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	return		

def addcdsorditem(v_wonum,v_part_no,v_date_requested,v_quote_desc,v_siteid):
	cdsorditemmbo.setValue("WONUM",v_wonum,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdsorditemmbo.setValue("SITEID",v_siteid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdsorditemmbo.setValue("ITEMNUM",v_part_no,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdsorditemmbo.setValue("DESCRIPTION",v_quote_desc,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdsorditemmbo.setValue("CATEGORY","Historic",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdsorditemmbo.setValue("ITEMSETID","ITEMSET",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdsorditemmbo.setValue("LINENUM",1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	cdsorditemmbo.setValue("DATE_REQ",v_date_requested,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	return

v_processed_status	= "PROCESSED"
v_error_status		= "ERROR"
v_orgid 			= "RRCDS"
v_siteid			= "BIRM"
v_error_msg			= "Item does not exist"


v_tablename 		= mbo.getName()
v_key 				= mbo.getString(str(v_tablename)+"ID") 
print "===========v_tablename==========="+str(v_tablename)
print "===========v_key==========="+str(v_key)
v_date 				= MXServer.getMXServer().getDate()


if(v_tablename == "CDS_CUST_ENQUIRY"):
	v_part_no 				= mbo.getString("PART_NO")
	v_date_requested 		= mbo.getDate("DATE_REQUESTED")
	v_quote_validity 		= mbo.getDate("QUOTE_VALIDITY")
	v_quote_ref 			= mbo.getString("QUOTE_REF")
	v_quote_qty_1 			= mbo.getString("QUOTE_QTY_1")
	v_quote_qty_2 			= mbo.getString("QUOTE_QTY_2")
	v_quote_qty_3 			= mbo.getString("QUOTE_QTY_3")
	v_quote_qty_4 			= mbo.getString("QUOTE_QTY_4")
	v_quote_price_1			= mbo.getString("QUOTE_PRICE_1")
	v_quote_price_2			= mbo.getString("QUOTE_PRICE_2")
	v_quote_price_3			= mbo.getString("QUOTE_PRICE_3")
	v_quote_price_4			= mbo.getString("QUOTE_PRICE_4")
	v_quote_price_lt_1		= mbo.getString("QUOTE_PRICE_LT_1")
	v_quote_price_lt_2		= mbo.getString("QUOTE_PRICE_LT_2")
	v_quote_price_lt_3		= mbo.getString("QUOTE_PRICE_LT_3")
	v_quote_price_lt_4		= mbo.getString("QUOTE_PRICE_LT_4")	
	v_quote_desc 			= "Quote Request Historic (AutoLoad) Ref "+str(v_quote_ref)+" Customer Enquiries "
	womboset 				= MXServer.getMXServer().getMboSet("WORKORDER", mbo.getUserInfo())
	wombo 					= womboset.add()
	
	addwo(wombo,v_part_no,v_date_requested,v_quote_validity,v_quote_desc,v_quote_qty_1,v_quote_qty_2,v_quote_qty_3,v_quote_qty_4,
			v_quote_price_1,v_quote_price_2,v_quote_price_3,v_quote_price_4,v_quote_price_lt_1,v_quote_price_lt_2,v_quote_price_lt_3,v_quote_price_lt_4)
	womboset.save()
	v_wonum = wombo.getString("WONUM")
	v_siteid =wombo.getString("SITEID")
	cdsorditemset 				= MXServer.getMXServer().getMboSet("CDS_ORD_ITEM", mbo.getUserInfo())
	cdsorditemmbo 				= cdsorditemset.add()
	addcdsorditem(v_wonum,v_part_no,v_date_requested,v_quote_desc,v_siteid)
	cdsorditemset.save()
	print "===========Processing CDS_CUST_ENQUIRY data ========="
	translog(v_key,v_processed_status,v_tablename,"")