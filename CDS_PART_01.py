#   Description:
#   CDS_PART_01.py
#   Script to calculate and update qty_available
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    15/12/2015
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                        N/A             A Rotaru
#
#    
#   Launch Point Variables
#   ----------------------
#   qty_allocated  IN
#   qty_on_hand    IN
#   qty_available  INOUT
#
#   Relationships
#   -------------
#

if qty_available <> qty_on_hand - qty_allocated:
    qty_available = qty_on_hand - qty_allocated