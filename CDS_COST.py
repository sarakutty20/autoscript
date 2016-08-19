#   Description:
#   CDS_COST.py
#   Calculate Cost by applying hourly rate
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    10/08/2016
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

commmboset = mbo.getMboSet("CDS_RATESPERHOUR.CDS_COMM_BURDENRATE")					
if(commmboset.moveFirst() is not None):							
	v_hourlyrate = commmboset.getMbo(0).getDouble("CDS_HOURLY_RATE")
	v_hours = mbo.getDouble("HOURS")
	v_cost =round((v_hours * v_hourlyrate),2)
mbo.setValue("COST",v_cost,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)