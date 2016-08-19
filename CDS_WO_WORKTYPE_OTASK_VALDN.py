#   Description:
#   CDS_WO_WORKTYPE_OTASK_VALDN.py
#   CDS Script for OTASK validation of data load
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
#   1.1      Changed to add error code to parent                      A Rotaru
#   1.2      Error fixing; added print statements                     A Rotaru
#   1.3.     Back to not adding error codes to parent				  A Rotaru
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
    print "correct otask and orditem"
    # Determine which part/product field to use for validation
    # First use product field if populated, otherwise use requested part number
    if mbo.getString("CDS_ITEMNUM") == "":
        print "cds_itemnum is null. getting the cds_ord_item row info"
        # use ordered part number
        ordMboSet = mbo.getMboSet("CDS_ORD_ITEM_ROW")
        ordItemMbo = ordMboSet.getMbo(0)                    # Always 1 record
        productToCheck = ordItemMbo.getString("ITEMNUM")    # item
    else:
        # use product number entered by user
        print "cds_itemnum exists. using this"
        productToCheck = mbo.getString("CDS_ITEMNUM")
        
    # Remove any existing errors
    woErrorSet = mbo.getMboSet("CDS_WO_ERROR")
    woErrorSet.deleteAll()

    # Check to see if product in CDS_PROD
    whereClause = "product_id = '" + productToCheck + "'"
    prodSet = mbo.getMboSet('$CDS_PRODS', 'CDS_PROD', whereClause)
    prod = prodSet.getMbo(0)

    # Initialise error tracking
    errorTrue = 0
        
    if prod == None:
        print "prod is none"

        # Check to see if product in CDS_PART
        whereClause = "part_nbr = '" + productToCheck + "'"
        partSet = mbo.getMboSet('$CDS_PARTS', 'CDS_PART', whereClause)
        part = partSet.getMbo(0)
        
        if part == None:
            print "part is none"
    
            # Check to see if product in CDS_PART_LEGACY
            whereClause = "part_nbr = '" + productToCheck + "'"
            partLegSet = mbo.getMboSet('$CDS_PART_LEGACYS', 'CDS_PART_LEGACY', whereClause)
            partLeg = partLegSet.getMbo(0)
            
            if partLeg == None:
                print "partleg is none"
                errorTrue = 1
                woError = woErrorSet.add()
                woError.setValue("WONUM",mbo.getString("WONUM"))
                woError.setValue("SITEID",mbo.getString("SITEID"))
                woError.setValue("DESCRIPTION", "Part does not exist in either Cincom or Legacy systems. Please verify part is correct.")
                woError.setValue("ERRORCODE","CDSERROR")
            else:
                print "partleg is not none"
                errorTrue = 1
                woError = woErrorSet.add()
                woError.setValue("WONUM",mbo.getString("WONUM"))
                woError.setValue("SITEID",mbo.getString("SITEID"))
                woError.setValue("DESCRIPTION", "Part only exists in Legacy system - " + partLeg.getString("DATA_SOURCE") + ". Please add Product/Part in Cincom.")
                woError.setValue("ERRORCODE","CDSERROR")

        else:
            print "part is not none"
            errorTrue = 1
            woError = woErrorSet.add()
            woError.setValue("WONUM",mbo.getString("WONUM"))
            woError.setValue("SITEID",mbo.getString("SITEID"))
            woError.setValue("DESCRIPTION", "Part only exists in Cincom. Please add Product in Cincom.")
            woError.setValue("ERRORCODE","CDSERROR")
        
    else: 
        print "prod is not none. setting cds_itemnum to "+productToCheck
        # Product exist in CDS_PROD
        mbo.setValue("CDS_ITEMNUM", productToCheck)

        # Set the HLevel1 values
        if mbo.getInt("CDS_HLEVEL") == 1:
            mbo.setValue("CDS_HLEVEL1_ITEMNUM", productToCheck)
            mbo.setValue("CDS_HLEVEL1_WONUM",mbo.getString("WONUM"))

    if errorTrue == 1:
        print "errorTrue is 1"
        mbo.setValue("CDS_ACMREFERENCE","CDSERROR")
    else:
        print "passed validation"
        # Passed validation, clear the error field
        mbo.setValue("CDS_ACMREFERENCE","")

    woErrorSet.save()
mbo.getThisMboSet().save()