#   Description:
#   CDS_WO_APPLYBURDENMARKUP.py
#   Apply burden rate and markup to gross totals
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    05/02/2016
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                            N/A         W Mahmud
#   1.1      Inculded purchase 
#				and manufacture breakdown               N/A        Saravanan
#   1.2      Included to apply different diff markup    N/A        Saravanan    
#   Launch Point Variables
#   ----------------------
#                                         Action launch point
#
#   Relationships
#   -------------
#   CDS_VENDOR2COMP
#   CDS_COMM_BURDENRATE

from java.util import Calendar 
from java.util import Date 
from psdi.app.report import ReportUtil 
from psdi.server import MXServer 
from psdi.mbo import MboConstants 
from psdi.mbo import SqlFormat


# Initialise defaults
v_cdscustmarkup = 0
v_burratepercen = 0
v_exchangerate 	= 0
v_makebuydecision = mbo.getString("CDS_MAKEBUY_DECISION")
v_different_markup = mbo.getString("CDS_DIFF_MARKUP")

# Set Markup
custmarkupmboset = mbo.getMboSet("CDS_VENDOR2COMP")
if (custmarkupmboset.moveFirst() is not None ):
    v_cdscustmarkup = custmarkupmboset.getMbo(0).getDouble("CDS_MARKUP")	
mbo.setValue("CDS_CUST_MARKUP",v_cdscustmarkup,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

if(v_makebuydecision  =="MAKE" and v_different_markup != ""):
	diffmarkupmboset = mbo.getMboSet("CDS_MARKUP_LIST")
	v_cdscustmarkup = diffmarkupmboset.getMbo(0).getDouble("PERCENTAGE")

# Set Burden Rate
commmboset = mbo.getMboSet("CDS_COMM_BURDENRATE")					
if(commmboset.moveFirst() is not None):							
    v_burratepercen = commmboset.getMbo(0).getDouble("CDS_BURDEN_RATE")
mbo.setValue("CDS_BURDEN_RATE",v_burratepercen,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)	

# Calculate Net Cost for each qty
for v_req_qty in range(1,5):
    v_unitcost = mbo.getDouble("CDS_COST_GROSS_QTY_" + str(v_req_qty))
    v_currencycode = mbo.getString("CDS_CUR_RES_QTY_" + str(v_req_qty))

    v_burdenrateonly = round((v_unitcost * (v_burratepercen/100.00)),2)	
    v_burplusunitcost = round(v_unitcost + (v_unitcost * (v_burratepercen/100.00)),2)	
    if(v_makebuydecision  =="MAKE"):
        v_burplusunitcost = v_unitcost	
    v_burwithmarkup = round(v_burplusunitcost + (v_burplusunitcost * (v_cdscustmarkup/100.00)),2)						
    v_exchangewhere = "currencycodeto ='USD' and sysdate between activedate and expiredate and currencycode = '"+str(v_currencycode)+"'"
    exchangeSet = mbo.getMboSet('$$EXCHANGE','EXCHANGE',v_exchangewhere)							 
    if(exchangeSet.moveFirst() is not None):					
        v_exchangerate = exchangeSet.getMbo(0).getDouble("EXCHANGERATE")
    elif(v_currencycode == "USD" ):
        v_exchangerate = 1
    else:
        v_exchangerate = 1
    v_costquote = round(v_exchangerate*v_burwithmarkup)
    v_burdenrateonly = round(v_exchangerate*v_burdenrateonly)
    # Set the cost values
    mbo.setValue("CDS_MARKUP_QTY"+str(v_req_qty),v_burwithmarkup,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    if(v_makebuydecision  != "MAKE"):	
		mbo.setValue("CDS_BURDEN_RATE_QTY"+str(v_req_qty),v_burplusunitcost,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("CDS_CONVRATE_QTY"+str(v_req_qty),v_exchangerate,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    mbo.setValue("CDS_COST_NET_QTY_"+str(v_req_qty),v_costquote,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    #mbo.setValue("CDS_COST_NET_QTY_"+str(v_req_qty),v_costquote - mbo.getDouble("CDS_COST_QTY_"+str(v_req_qty)+"_NREC"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)	
    mbo.setValue("CDS_COST_BUR_PERCENT_QTY_"+str(v_req_qty),v_burdenrateonly,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

# Set quote validity
c = Calendar.getInstance() 
c.add(Calendar.MONTH,12)
d = c.getTime()
mbo.setValue("CDS_QUOTE_VALIDITY",d,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

v_hlevel = mbo.getInt("CDS_HLEVEL")
if(v_hlevel == 1):
	v_hlevel1_wo  = mbo.getString("WONUM")
	v_manufwhereclause = "istask = 0 and cds_quote_type = 'FORMAL' and cds_makebuy_decision = 'MAKE' start with wonum = '"+str(v_hlevel1_wo)+"' connect by PRIOR wonum = parent"
	womanufmboset = mbo.getMboSet("$$WORKORDERMANUF","WORKORDER",v_manufwhereclause)
	if(womanufmboset.moveFirst() is not None):
		#mbo.getFloat("CDS_COST_QTY_1_NREC")+mbo.getFloat("CDS_COST_QTY_1_REC")+mbo.getFloat("CDS_QUOTE_QTY_1")
		#mbo.getInt("CDS_LEADTIME_QTY_1_NREC")+mbo.getInt("CDS_LEADTIME_QTY_1_REC")
		
		v_tot_manuf_lt_qty_1 = womanufmboset.sum("CDS_LEADTIME_QTY_1_NREC")+womanufmboset.sum("CDS_LEADTIME_QTY_1_REC")
		v_tot_manuf_lt_qty_2 = womanufmboset.sum("CDS_LEADTIME_QTY_2_NREC")+womanufmboset.sum("CDS_LEADTIME_QTY_2_REC")
		v_tot_manuf_lt_qty_3 = womanufmboset.sum("CDS_LEADTIME_QTY_3_NREC")+womanufmboset.sum("CDS_LEADTIME_QTY_3_REC")
		v_tot_manuf_lt_qty_4 = womanufmboset.sum("CDS_LEADTIME_QTY_4_NREC")+womanufmboset.sum("CDS_LEADTIME_QTY_4_REC")
		
		
		v_tot_manuf_nonrec_cost_qty_1 = womanufmboset.sum("CDS_COST_QTY_1_NREC")
		v_tot_manuf_nonrec_cost_qty_2 = womanufmboset.sum("CDS_COST_QTY_2_NREC")
		v_tot_manuf_nonrec_cost_qty_3 = womanufmboset.sum("CDS_COST_QTY_3_NREC")
		v_tot_manuf_nonrec_cost_qty_4 = womanufmboset.sum("CDS_COST_QTY_4_NREC")
		
		mbo.setValue("CDS_COST_NET_QTY_1",mbo.getDouble("CDS_COST_NET_QTY_1")-v_tot_manuf_nonrec_cost_qty_1)
		mbo.setValue("CDS_COST_NET_QTY_2",mbo.getDouble("CDS_COST_NET_QTY_2")-v_tot_manuf_nonrec_cost_qty_2)
		mbo.setValue("CDS_COST_NET_QTY_3",mbo.getDouble("CDS_COST_NET_QTY_3")-v_tot_manuf_nonrec_cost_qty_3)
		mbo.setValue("CDS_COST_NET_QTY_4",mbo.getDouble("CDS_COST_NET_QTY_4")-v_tot_manuf_nonrec_cost_qty_4)		
		
		v_tot_manuf_cost_qty_1 = womanufmboset.sum("CDS_COST_QTY_1_NREC")+womanufmboset.sum("CDS_COST_QTY_1_REC")
		v_tot_manuf_cost_qty_2 = womanufmboset.sum("CDS_COST_QTY_2_NREC")+womanufmboset.sum("CDS_COST_QTY_2_REC")
		v_tot_manuf_cost_qty_3 = womanufmboset.sum("CDS_COST_QTY_3_NREC")+womanufmboset.sum("CDS_COST_QTY_3_REC")
		v_tot_manuf_cost_qty_4 = womanufmboset.sum("CDS_COST_QTY_4_NREC")+womanufmboset.sum("CDS_COST_QTY_4_REC")
		mbo.setValue("CDS_TOT_MANUF_LEADTIME_QTY_1",v_tot_manuf_lt_qty_1)
		mbo.setValue("CDS_TOT_MANUF_LEADTIME_QTY_2",v_tot_manuf_lt_qty_2)
		mbo.setValue("CDS_TOT_MANUF_LEADTIME_QTY_3",v_tot_manuf_lt_qty_3)
		mbo.setValue("CDS_TOT_MANUF_LEADTIME_QTY_4",v_tot_manuf_lt_qty_4)
		
		mbo.setValue("CDS_TOT_MANUF_COST_QTY_1",v_tot_manuf_cost_qty_1)
		mbo.setValue("CDS_TOT_MANUF_COST_QTY_2",v_tot_manuf_cost_qty_2)
		mbo.setValue("CDS_TOT_MANUF_COST_QTY_3",v_tot_manuf_cost_qty_3)
		mbo.setValue("CDS_TOT_MANUF_COST_QTY_4",v_tot_manuf_cost_qty_4)
		
	v_purwhereclause = "istask = 0 and ((cds_quote_type = 'FORMAL' and cds_makebuy_decision = 'BUY') or cds_quote_type = 'LIGHT' ) start with wonum = '"+str(v_hlevel1_wo)+"' connect by PRIOR wonum = parent"
	wopurmboset = mbo.getMboSet("$$WORKORDERPUR","WORKORDER",v_purwhereclause)
	if(wopurmboset.moveFirst() is not None):
		v_tot_pur_lt_qty_1 = wopurmboset.sum("CDS_LEADTIME_QTY_1_NREC")+wopurmboset.sum("CDS_LEADTIME_QTY_1_REC")+wopurmboset.sum("CDS_QUOTE_LEADTIME_QTY_1")
		v_tot_pur_lt_qty_2 = wopurmboset.sum("CDS_LEADTIME_QTY_2_NREC")+wopurmboset.sum("CDS_LEADTIME_QTY_2_REC")+wopurmboset.sum("CDS_QUOTE_LEADTIME_QTY_2")
		v_tot_pur_lt_qty_3 = wopurmboset.sum("CDS_LEADTIME_QTY_3_NREC")+wopurmboset.sum("CDS_LEADTIME_QTY_3_REC")+wopurmboset.sum("CDS_QUOTE_LEADTIME_QTY_3")
		v_tot_pur_lt_qty_4 = wopurmboset.sum("CDS_LEADTIME_QTY_4_NREC")+wopurmboset.sum("CDS_LEADTIME_QTY_4_REC")+wopurmboset.sum("CDS_QUOTE_LEADTIME_QTY_4")
		
		v_tot_pur_cost_qty_1 = wopurmboset.sum("CDS_COST_QTY_1_NREC")+wopurmboset.sum("CDS_COST_QTY_1_REC")+wopurmboset.sum("CDS_QUOTE_QTY_1")
		v_tot_pur_cost_qty_2 = wopurmboset.sum("CDS_COST_QTY_2_NREC")+wopurmboset.sum("CDS_COST_QTY_2_REC")+wopurmboset.sum("CDS_QUOTE_QTY_2")
		v_tot_pur_cost_qty_3 = wopurmboset.sum("CDS_COST_QTY_3_NREC")+wopurmboset.sum("CDS_COST_QTY_3_REC")+wopurmboset.sum("CDS_QUOTE_QTY_3")
		v_tot_pur_cost_qty_4 = wopurmboset.sum("CDS_COST_QTY_4_NREC")+wopurmboset.sum("CDS_COST_QTY_4_REC")+wopurmboset.sum("CDS_QUOTE_QTY_4")
		
		mbo.setValue("CDS_TOT_PURC_LEADTIME_QTY_1",v_tot_pur_lt_qty_1)
		mbo.setValue("CDS_TOT_PURC_LEADTIME_QTY_2",v_tot_pur_lt_qty_2)
		mbo.setValue("CDS_TOT_PURC_LEADTIME_QTY_3",v_tot_pur_lt_qty_3)
		mbo.setValue("CDS_TOT_PURC_LEADTIME_QTY_4",v_tot_pur_lt_qty_4)
		
		v_tot_pur_nonrec_cost_qty_1 = wopurmboset.sum("CDS_COST_QTY_1_NREC")
		v_tot_pur_nonrec_cost_qty_2 = wopurmboset.sum("CDS_COST_QTY_2_NREC")
		v_tot_pur_nonrec_cost_qty_3 = wopurmboset.sum("CDS_COST_QTY_3_NREC")
		v_tot_pur_nonrec_cost_qty_4 = wopurmboset.sum("CDS_COST_QTY_4_NREC")
		
		v_tot_burdenrate_only_qty_1 = wopurmboset.sum("CDS_COST_BUR_PERCENT_QTY_1")
		v_tot_burdenrate_only_qty_2 = wopurmboset.sum("CDS_COST_BUR_PERCENT_QTY_2")
		v_tot_burdenrate_only_qty_3 = wopurmboset.sum("CDS_COST_BUR_PERCENT_QTY_3")
		v_tot_burdenrate_only_qty_4 = wopurmboset.sum("CDS_COST_BUR_PERCENT_QTY_4")

		mbo.setValue("CDS_COST_NET_QTY_1",mbo.getDouble("CDS_COST_NET_QTY_1")-v_tot_pur_nonrec_cost_qty_1+v_tot_burdenrate_only_qty_1)
		mbo.setValue("CDS_COST_NET_QTY_2",mbo.getDouble("CDS_COST_NET_QTY_2")-v_tot_pur_nonrec_cost_qty_2+v_tot_burdenrate_only_qty_2)
		mbo.setValue("CDS_COST_NET_QTY_3",mbo.getDouble("CDS_COST_NET_QTY_3")-v_tot_pur_nonrec_cost_qty_3+v_tot_burdenrate_only_qty_3)
		mbo.setValue("CDS_COST_NET_QTY_4",mbo.getDouble("CDS_COST_NET_QTY_4")-v_tot_pur_nonrec_cost_qty_4+v_tot_burdenrate_only_qty_4)	
	
		mbo.setValue("CDS_TOT_PURC_COST_QTY_1",v_tot_pur_cost_qty_1)
		mbo.setValue("CDS_TOT_PURC_COST_QTY_2",v_tot_pur_cost_qty_2)
		mbo.setValue("CDS_TOT_PURC_COST_QTY_3",v_tot_pur_cost_qty_3)
		mbo.setValue("CDS_TOT_PURC_COST_QTY_4",v_tot_pur_cost_qty_4)
mbo.getThisMboSet().save()