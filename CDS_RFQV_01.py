#   Description:
#   CDS_RFQV_01.py
#   Setting report sent value to be zero when the rfq duplicate
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    25/11/2015
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                            N/A          S Ananthan
#
#    
#   Launch Point Variables
#   ----------------------
#                                         Action launch point
#
#   Relationships
#   -------------

if(mbo.isNew() == True):
 mbo.setValue("CDS_RPTSENT",0,7L)