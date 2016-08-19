#   Description:
#   CDS_WO_02.py
#   Creation of Ordered Items Child WOs
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    13/10/2015
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                        N/A             A Rotaru
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

ordItemMboSet = mbo.getMboSet("CDS_ORD_ITEM")
childMboSet = mbo.getMboSet("CHILDNOTASK")
ordItemCount = ordItemMboSet.count()

if (ordItemCount > 0 ):
    topdescription = mbo.getString("CDS_CUSTOMER") + " Quote Request " + mbo.getString("CDS_CUSTOMER_REF_NO") + " - automatically loaded"
    mbo.setValue("DESCRIPTION",topdescription)
    mbo.setValue("WORKTYPE","WKSCP")
    i=0
    while (i < ordItemCount):
        ordItemMbo = ordItemMboSet.getMbo(i)
        childMbo = childMboSet.add()
        orditem = ordItemMbo.getString("ITEMNUM")
        linenum = ordItemMbo.getString("LINENUM")
        childMbo.setValue("PARENT",mbo.getString("WONUM"))
        childMbo.setValue("ORGID",mbo.getString("ORGID"))
        childMbo.setValue("CDS_CUSTOMER_REF_NO",mbo.getString("CDS_CUSTOMER_REF_NO"))
        childMbo.setValue("CDS_CUSTOMER",mbo.getString("CDS_CUSTOMER"))
        childMbo.setValue("CDS_ITEMSETID","ITEMSET")
        childMbo.setValue("WORKTYPE","OTASK")
        childMbo.setValue("CDS_OP_TYPE","ORDITEM")
        childMbo.setValue("DESCRIPTION","Quote Request for Item " + orditem + " - Line " + linenum)
        childMbo.setValue("WOSEQUENCE",linenum)
        childMbo.setValue("REQ_QTY_1",ordItemMbo.getInt("REQ_QTY_1"))
        childMbo.setValue("REQ_QTY_2",ordItemMbo.getInt("REQ_QTY_2"))
        childMbo.setValue("REQ_QTY_3",ordItemMbo.getInt("REQ_QTY_3"))
        childMbo.setValue("REQ_QTY_4",ordItemMbo.getInt("REQ_QTY_4"))
        childMbo.setValue("CDS_HLEVEL","1")
        childMbo.setValue("CDS_HLEVEL_STR","-1")
        # Determine BOM display sequence
        # Assume 5 hierarchy levels at most of BOM
        MAX_BOM_LEVEL = 5
        CHAR_PER_LEVEL = 3
        bomdispseq = str(linenum).zfill(CHAR_PER_LEVEL)
        bomdispseq = bomdispseq.ljust(MAX_BOM_LEVEL*CHAR_PER_LEVEL,"0")
        childMbo.setValue("CDS_BOM_DISP_SEQ_STR", bomdispseq)

        i=i+1