#   Description:
#   CDS_PART2ITEM.py
#   Insert/Update into ITEMMASTER ,ITEMORGINFO and COMMODITIES after CDS_PART table has been inserted/updated 
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    07/07/2016
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
	cdstranslogset.save()
	return
	
def addcomm(commSet,v_comm,v_commgroup,v_srvtype,v_setid):
	#print "======Add commodity ============"
	#print "======Add commodity ===v_comm========="+str(v_comm)
	#print "======Add commodity ===v_commgroup========="+str(v_commgroup)
	# psdi.app.item.Commodity java expects the reference of Parent application . So, it needs to be set parent application as ITEM.
	commSet.setParentApp("ITEM")
	commmbo = commSet.add()	
	commmbo.setValue("COMMODITY",v_comm,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	commmbo.setValue("DESCRIPTION",v_comm,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	commmbo.setValue("PARENT",v_commgroup,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	commmbo.setValue("SERVICETYPE",v_srvtype,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	commmbo.setValue("ITEMSETID",v_setid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	commmbo.setValue("ISSERVICE",False,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
	return	

v_tablename 		= "CDS_PART"
v_processed_status	= "PROCESSED"
v_error_status		= "ERROR"
v_status_pending 	= "PENDING"
v_status_active 	= "ACTIVE"
v_comment 			= "Automatically Set "
v_lottype 			= "NOLOT"
v_itemsetid 		= "ITEMSET"
v_orgid 			= "RRCDS"
v_category_stk 		= "STK"
v_servicetype 		= "PROCURE"


v_key 				= mbo.getString('CDS_PARTID') 
v_date 				= MXServer.getMXServer().getDate()
v_part_nbr 			= mbo.getString('PART_NBR') 
v_part_desc 		= mbo.getString('PART_DESC') 
v_part_type 		= mbo.getString('PART_TYPE') 
v_qty_on_hand 		= mbo.getString('QTY_ON_HAND') 
v_qty_allocated 	= mbo.getString('QTY_ALLOCATED') 
v_qty_available 	= mbo.getString('QTY_AVAILABLE') 
v_lead_time 		= mbo.getString('LEAD_TIME') 
v_date_last_update 	= mbo.getDate('DATE_LAST_UPDATE') 
v_user_field_1 		= mbo.getString('USER_FIELD_1') 
v_commoditygroup 	= v_user_field_1[0:2]
v_commodity 		= v_user_field_1[2:2+len(v_user_field_1)]
v_errormsg			= "Commodity Group  "+str(v_commoditygroup)+"  is not valid "



if(v_commoditygroup != 'SS' and v_commoditygroup != 'Y-'):
	print "Commodity group is invalid "
	translog(v_key,v_error_status,v_tablename,v_errormsg)

else: 
	print "Commodity group is either SS or Y- ===================="

	v_whereclausecomm = "commodity = '"+str(v_commodity)+"'"
	commSet = mbo.getMboSet('$$COMMODITIES','COMMODITIES',v_whereclausecomm)

	v_whereclausecomm1 = "commodity = '"+str(v_user_field_1)+"'"
	commSet1 = mbo.getMboSet('$$COMMODITIES1','COMMODITIES',v_whereclausecomm1)
	v_boolean = False
	
	print "Count =======commSet.count===  "+str(commSet.count())
	print "Count =======commSet1.count===  "+str(commSet1.count())
	# condition for if commodity code and user field are same 
	if(commSet1.count() > 0):
		v_commodity = v_user_field_1
	# To create new commodity code 	if the commodity code exists in another commodity group 
	if(commSet.moveFirst() is not None):
		print "v_commodity========="+str(v_commodity)
		print "v_user_field_1========="+str(v_user_field_1)
		commmbo = commSet.getMbo(0)
		v_commoditytb = commmbo.getString("COMMODITY")
		v_parent = commmbo.getString("PARENT")
		if(v_parent != v_commoditygroup and commSet1.count() == 0):
			print "v_parent========="+str(v_parent)
			print "v_commoditygroup========="+str(v_commoditygroup)
			print "v_user_field_1========="+str(v_user_field_1)
			addcomm(commSet,v_user_field_1,v_commoditygroup,v_servicetype,v_itemsetid)
			v_boolean = True
	# Commodity if not exist then create new commodity code 		
	if(commSet1.count() == 0 and commSet.count() == 0):
		print "=====================New Commodity code will create and update into Item"
		addcomm(commSet,v_commodity,v_commoditygroup,v_servicetype,v_itemsetid)
	
	v_whereclauseql = "itemnum = '"+str(v_part_nbr)+"'"
	itemSet = mbo.getMboSet('$$ITEM','ITEM',v_whereclauseql)
  
	itemmbo = itemSet.moveFirst()
	if(itemmbo is not None):    
		print '********Itemnum exist in Maximo and update DESCRIPTION,COMMODITYGROUP COMMODITY - CDS_PART2ITEM Inside  if **************************'
		itemmbo.setValue("DESCRIPTION",v_part_desc,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		itemmbo.setValue("COMMODITYGROUP",v_commoditygroup,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		#If commodity code exists and recently created 
		if(v_boolean):
			v_commodity = v_user_field_1
		itemmbo.setValue("COMMODITY",v_commodity,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)	
	elif(itemSet.isEmpty()):
		print '********CDS_PART2ITEM Inside  else CREATE ITEM **************************'
		print '********CDS_PART2ITEM Create new item with reference of part number *********'+str(v_part_nbr)
		itemmbo = itemSet.add()	
		itemmbo.setValue("ITEMNUM",v_part_nbr,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		itemmbo.setValue("DESCRIPTION",v_part_desc,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		itemmbo.setValue("COMMODITYGROUP",v_commoditygroup,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		#If commodity code exists and recently created 
		if(v_boolean):
			v_commodity = v_user_field_1
		itemmbo.setValue("COMMODITY",v_commodity,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		itemmbo.setValue("STATUS",v_status_pending,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		itemmbo.setValue("LOTTYPE",v_lottype,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		itemmbo.setValue("ITEMSETID",v_itemsetid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		itemorginfomboset = itemmbo.getMboSet("ITEMORGINFO")
		itemorginfombo = itemorginfomboset.add()
		itemorginfombo.setValue("ITEMNUM",v_part_nbr)
		itemorginfombo.setValue("ITEMSETID",v_itemsetid,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		itemorginfombo.setValue("STATUS",v_status_pending)
		itemorginfombo.setValue("ORGID",v_orgid)
		itemorginfombo.setValue("CATEGORY",v_category_stk,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
		itemmbo.changeStatus(v_status_active, MXServer.getMXServer().getDate(),v_comment)
		itemorginfombo.changeStatus(v_status_active, MXServer.getMXServer().getDate(),v_comment)
	translog(v_key,v_processed_status,v_tablename,"")