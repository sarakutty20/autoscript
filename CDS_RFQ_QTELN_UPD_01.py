#   Description:
#   CDS_RFQ_QTELN_UPD_01.py
#   Quotline Update after RFQ completed 
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    30/11/2015
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                            N/A         S Ananthan
#   1.1      Add change status to QUOTECOMP                         A Rotaru
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
v_quotereqlinenum = mbo.getString("RFQ1")

v_whereclauseql = "siteid = '"+str(v_siteid)+"' and wonum = '"+str(v_quotereqlinenum)+"' and CDS_QUOTE_TYPE in ('FORMAL','LIGHT')"
quoteldrlineSet = mbo.getMboSet('$$WO','WORKORDER',v_whereclauseql)
#print '******** Inside CDS_RFQ_QTELN_UPD_01.py **************************'    
qldrlinembo = quoteldrlineSet.moveFirst()
if(qldrlinembo is not None):    
    #print '******** Inside for qldrlinembo **************************'
    v_whereqline = "siteid = '"+str(v_siteid)+"' and rfqnum = '"+str(v_rfqnum)+"' and isawarded = 1 "
    rfqqtnlineSet = mbo.getMboSet('$$RFQQL','QUOTATIONLINE',v_whereqline)
    #print "----------------"+str(v_whereqline)
    c = Calendar.getInstance() 
    c.add(Calendar.MONTH,12)
    d = c.getTime()
    qldrlinembo.setValue("CDS_QUOTE_VALIDITY",d,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    if(rfqqtnlineSet.moveFirst() is not None):
        for j in range(0,rfqqtnlineSet.count()):                    
            rfqqtnlinembo = rfqqtnlineSet.getMbo(j)                
            v_req_qty = rfqqtnlinembo.getMboSet("RFQLINE").getMbo(0).getInt("REQ_QTY_NUM")
            v_unitcost = rfqqtnlinembo.getDouble("UNITCOST")
            v_currencycode = rfqqtnlinembo.getMboSet("RFQVENDOR").getMbo(0).getString("CURRENCYCODE")                        
            v_leadtime = rfqqtnlinembo.getDouble("CDS_LEAD_TIME")
            qldrlinembo.setValue("CDS_QUOTE_QTY_"+str(v_req_qty),v_unitcost,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            qldrlinembo.setValue("CDS_CUR_RES_QTY_"+str(v_req_qty),v_currencycode,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            qldrlinembo.setValue("CDS_COST_GROSS_QTY_"+str(v_req_qty),v_unitcost,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            qldrlinembo.setValue("CDS_QUOTE_LEADTIME_QTY_"+str(v_req_qty),v_leadtime,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            qldrlinembo.setValue("CDS_LEADTIME_QTY_"+str(v_req_qty),v_leadtime,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)

    if qldrlinembo.getString("STATUS") != "QUOTECOMP":
        qldrlinembo.changeStatus("QUOTECOMP", MXServer.getMXServer().getDate(),"Automatic status")

    # Apply Markup/Burden rate by calling action
    try:
        actionSet = MXServer.getMXServer().getMboSet("action", mbo.getUserInfo());
        sqf = SqlFormat("action = :1")
        sqf.setObject(1, "action", "action", "CDS_WO_APPLYBURDENMARKUP")

        actionSet.setWhere(sqf.format())
        actionSet.reset()
        actionSet.getMbo(0).executeAction(qldrlinembo)
    except:
        print "Exception: ", sys.exc_info()

    quoteldrlineSet.save()