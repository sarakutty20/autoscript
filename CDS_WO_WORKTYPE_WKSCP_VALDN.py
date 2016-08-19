#   Description:
#   CDS_WO_WORKTYPE_WKSCP_VALDN.py
#   CDS Script for WKSCP validation of data load
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    01/10/2015
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                            N/A           W Mahmud
#   1.1      Clear error flag from parent                             A Rotaru
#   1.2      Add customer communication functionality                 A Rotaru
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

if mbo.getString("WORKTYPE") == "WKSCP":
    # reset the error field
    mbo.setValue("CDS_ACMREFERENCE","")
    
    childMboSet = mbo.getMboSet("CHILDNOTASK")
    ordItemCount = childMboSet.count()
    if (ordItemCount > 0):
        i=0
        mboErrorTrue = 0
        while (i < ordItemCount):
            ordItemMbo = childMboSet.getMbo(i)
            if ordItemMbo.getString("WORKTYPE") == "OTASK" and ordItemMbo.getString("CDS_OP_TYPE") == "ORDITEM":
                errorTrue = 0
                # Remove any existing errors
                woErrorSet = ordItemMbo.getMboSet("CDS_WO_ERROR")
                woErrorSet.deleteAll()

                if ordItemMbo.getInt("REQ_QTY_1") < 0:
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_1 has a value below zero")
                    woError.setValue("ERRORCODE","CUSTERROR")
                if ordItemMbo.getInt("REQ_QTY_2") < 0:
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_2 has a value below zero")
                    woError.setValue("ERRORCODE","CUSTERROR")
                if ordItemMbo.getInt("REQ_QTY_3") < 0:
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_3 has a value below zero")
                    woError.setValue("ERRORCODE","CUSTERROR")
                if ordItemMbo.getInt("REQ_QTY_4") < 0:
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_4 has a value below zero")
                    woError.setValue("ERRORCODE","CUSTERROR")
                if ordItemMbo.getInt("REQ_QTY_1") == 0:
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_1 must be higher than zero")
                    woError.setValue("ERRORCODE","CUSTERROR")
                if ordItemMbo.getInt("REQ_QTY_2") > 0 and ordItemMbo.getInt("REQ_QTY_1") > 0 and ordItemMbo.getInt("REQ_QTY_2") <= ordItemMbo.getInt("REQ_QTY_1"):
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_2 is smaller or equal to REQ_QTY_1")
                    woError.setValue("ERRORCODE","CUSTERROR")
                if ordItemMbo.getInt("REQ_QTY_3") > 0 and ordItemMbo.getInt("REQ_QTY_2") == 0:
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_2 is empty when REQ_QTY_3 is populated")
                    woError.setValue("ERRORCODE","CUSTERROR")
                if ordItemMbo.getInt("REQ_QTY_3") > 0 and ordItemMbo.getInt("REQ_QTY_2") > 0 and ordItemMbo.getInt("REQ_QTY_3") <= ordItemMbo.getInt("REQ_QTY_2"):
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_3 is smaller or equal to REQ_QTY_2")
                    woError.setValue("ERRORCODE","CUSTERROR")
                if ordItemMbo.getInt("REQ_QTY_4") > 0 and ordItemMbo.getInt("REQ_QTY_3") == 0:
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_3 is empty when REQ_QTY_4 is populated")
                    woError.setValue("ERRORCODE","CUSTERROR")
                if ordItemMbo.getInt("REQ_QTY_4") > 0 and ordItemMbo.getInt("REQ_QTY_3") > 0 and ordItemMbo.getInt("REQ_QTY_4") <= ordItemMbo.getInt("REQ_QTY_3"):
                    errorTrue = 1
                    woError = woErrorSet.add()
                    woError.setValue("WONUM",ordItemMbo.getString("WONUM"))
                    woError.setValue("SITEID",ordItemMbo.getString("SITEID"))
                    woError.setValue("DESCRIPTION","REQ_QTY_4 is smaller or equal to REQ_QTY_3")
                    woError.setValue("ERRORCODE","CUSTERROR")

                # Update the error flags
                if errorTrue == 1:
                    mboErrorTrue = 1
                    ordItemMbo.setValue("CDS_ACMREFERENCE","CUSTERROR")
                else:
                    # Passed validation, the error field
                    ordItemMbo.setValue("CDS_ACMREFERENCE","")
            i = i + 1

        # Set the mbo error flag
        if mboErrorTrue == 1:
            mbo.setValue("CDS_ACMREFERENCE","CUSTERROR")
            ctMboSet = mbo.getMboSet("$commtemp","COMMTEMPLATE","TEMPLATEID ='CDS_001'");
            ctMboSet.setQbeExactMatch("true")
            ctMboSet.reset()
            ctMbo = ctMboSet.getMbo(0)
            if(ctMbo is not None):
                ctMbo.sendMessage(mbo,mbo);
        else:
            mbo.setValue("CDS_ACMREFERENCE","")