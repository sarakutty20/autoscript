#   Description:
#   CDS_WO_ME.py
#   Creation of Ordered Items Child WOs
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    13/01/2016
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                        N/A             S Ananthan
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
from psdi.mbo import MboValue
from psdi.mbo import MboConstants
from psdi.app.workorder import WO
from psdi.server import MXServer
from java.util import Calendar
from java.util import Date

billMboSet = mbo.getMboSet("CDS_BILL")
childMboSet = mbo.getMboSet("CHILDNOTASK")
d=Calendar.getInstance()

if(billMboSet.moveFirst() is not None):
    v_hlevel = mbo.getInt("CDS_HLEVEL") + 1
    rootpart = mbo.getString("CDS_HLEVEL1_ITEMNUM")
    parentbomseq = mbo.getString("CDS_BOM_DISP_SEQ_STR")
    for i in range(0,billMboSet.count()):
        billmbo = billMboSet.getMbo(i)
        partnbr = billmbo.getString("COMP_PART_NBR")
        wosequnce = i + 1
        qtyper = billmbo.getInt("QTY_PER")
        childMbo = childMboSet.add() 
        childMbo.setValue("PARENT",mbo.getString("WONUM"))
        childMbo.setValue("PARENTCHGSSTATUS",0)                                                 # Force so that the child does not change status when parent status changes
        childMbo.setValue("ORGID",mbo.getString("ORGID"))
        childMbo.setValue("CDS_CUSTOMER_REF_NO",mbo.getString("CDS_CUSTOMER_REF_NO"))
        childMbo.setValue("CDS_CUSTOMER",mbo.getString("CDS_CUSTOMER"))
        childMbo.setValue("CDS_ITEMSETID","ITEMSET")
        childMbo.setValue("CDS_ITEMNUM",partnbr)
        childMbo.setValue("CDS_HLEVEL1_WONUM",mbo.getString("CDS_HLEVEL1_WONUM"))
        childMbo.setValue("CDS_HLEVEL1_ITEMNUM",rootpart)
        childMbo.setValue("CDS_HLEVEL",v_hlevel)
        childMbo.setValue("CDS_OP_TYPE",mbo.getString("CDS_OP_TYPE"))
        childMbo.setValue("WORKTYPE",mbo.getString("WORKTYPE"))         
        childMbo.setValue("DESCRIPTION","Quote Request for Item " + partnbr + " (" + rootpart + " - Level " + str(v_hlevel) + ")")
        childMbo.setValue("WOSEQUENCE",wosequnce)
        childMbo.setValue("REQ_QTY_1",mbo.getInt("REQ_QTY_1") * qtyper)
        childMbo.setValue("REQ_QTY_2",mbo.getInt("REQ_QTY_2") * qtyper)
        childMbo.setValue("REQ_QTY_3",mbo.getInt("REQ_QTY_3") * qtyper)
        childMbo.setValue("REQ_QTY_4",mbo.getInt("REQ_QTY_4") * qtyper)
        childMbo.setValue("TARGCOMPDATE",mbo.getString("TARGCOMPDATE"))
        v_finallevel = []    
        for j in range(0,v_hlevel):
            v_finallevel.append("-")
        v_finallevel.append(str(v_hlevel)) 
        childMbo.setValue("CDS_HLEVEL_STR",''.join(v_finallevel))
        
        # Determine BOM display sequence
        # Assume 5 hierarchy levels at most of BOM
        MAX_BOM_LEVEL = 5
        CHAR_PER_LEVEL = 3
        bomdispseq = str(parentbomseq[:(v_hlevel-1)*CHAR_PER_LEVEL] + str(wosequnce).zfill(CHAR_PER_LEVEL))
        bomdispseq = bomdispseq.ljust(MAX_BOM_LEVEL*CHAR_PER_LEVEL,"0")
        childMbo.setValue("CDS_BOM_DISP_SEQ_STR", bomdispseq)
        
        childMbo.changeStatus("LOADED", MXServer.getMXServer().getDate(), "Child workorder")
    childMboSet.save()