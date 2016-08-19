#   Description:
#   CDS_WO_POPULATE_QUOTE_REQUEST.py
#   CDS Script to populate quote for quantities based on quote categorisation
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    21/10/2015
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                            N/A           W Mahmud
#
#    
#   Launch Point Variables
#   ----------------------
#                                         Action launch point
#
#   Relationships
#   -------------
#

from psdi.mbo import Mbo
from psdi.mbo import MboRemote 
from psdi.mbo import MboSet
from psdi.mbo import MboConstants
from psdi.server import MXServer

if mbo.getString("WORKTYPE") == "OTASK" and mbo.getString("CDS_OP_TYPE") == "ORDITEM":
    # Get quote type
    quoteType = mbo.getString("CDS_QUOTE_TYPE")
    reqqty1 = mbo.getInt("REQ_QTY_1")
    reqqty2 = mbo.getInt("REQ_QTY_2")
    reqqty3 = mbo.getInt("REQ_QTY_3")
    reqqty4 = mbo.getInt("REQ_QTY_4")
    
    if quoteType == "ROM" or quoteType == "UNIT" or quoteType == "DLF" or quoteType == "STOCK":
    
        partMboSet = mbo.getMboSet("CDS_ITEM.CDS_PROD.CDS_PART")
        partMbo = partMboSet.getMbo(0)                          # Always 1 record
        
        
        if quoteType == "ROM":        
            unitPrice = 0                                       # Commercial to update quote
            leadTime = partMbo.getInt("LEAD_TIME")

        elif quoteType == "UNIT":
            unitPrice = 0                                       # Commercial to update quote
            leadTime = partMbo.getInt("LEAD_TIME")

        elif quoteType == "DLF":
            # Retrieve DLF Price for part
            dlfSet = partMbo.getMboSet("CDS_DLF")
            dlfMbo = dlfSet.getMbo(0)                           # Always 1 record
            unitPrice = dlfMbo.getFloat("PRICE")
            leadTime = dlfMbo.getInt("LEAD_TIME")								

        elif quoteType == "STOCK":
            # Retrieve STOCK Price for part
            cprtSet = partMbo.getMboSet("CDS_CPRT")
            cprtMbo = cprtSet.getMbo(0)                         # Always 1 record
            unitPrice = cprtMbo.getFloat("ACCUM_STD_TOTAL_COST")
            leadTime = partMbo.getInt("LEAD_TIME")			
            
        # Update quote quantities/Lead Time
        if (reqqty1 > 0):
            mbo.setValue("CDS_QUOTE_QTY_1", unitPrice)
            mbo.setValue("CDS_COST_GROSS_QTY_1",unitPrice,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("CDS_CUR_RES_QTY_1","USD",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("CDS_QUOTE_LEADTIME_QTY_1", leadTime)
            mbo.setValue("CDS_LEADTIME_QTY_1", leadTime)
        if (reqqty2 > 0):
            mbo.setValue("CDS_QUOTE_QTY_2", unitPrice)
            mbo.setValue("CDS_COST_GROSS_QTY_2",unitPrice,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("CDS_CUR_RES_QTY_2","USD",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("CDS_QUOTE_LEADTIME_QTY_2", leadTime)
            mbo.setValue("CDS_LEADTIME_QTY_2", leadTime)
        if (reqqty3 > 0):
            mbo.setValue("CDS_QUOTE_QTY_3", unitPrice)
            mbo.setValue("CDS_COST_GROSS_QTY_3",unitPrice,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("CDS_CUR_RES_QTY_3","USD",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("CDS_QUOTE_LEADTIME_QTY_3", leadTime)
            mbo.setValue("CDS_LEADTIME_QTY_3", leadTime)
        if (reqqty4 > 0):
            mbo.setValue("CDS_QUOTE_QTY_4", unitPrice)
            mbo.setValue("CDS_COST_GROSS_QTY_4",unitPrice,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("CDS_CUR_RES_QTY_4","USD",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
            mbo.setValue("CDS_QUOTE_LEADTIME_QTY_4", leadTime)
            mbo.setValue("CDS_LEADTIME_QTY_4", leadTime)