#   Description:
#   CDS_WO_JPNUM.py
#   To set JPNUM 
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    16/12/2015
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                            N/A          S Ananthan
#    
#   Launch Point Variables
#   ----------------------
#                                         Action launch point
#
#   Relationships
#   -------------


from psdi.mbo import Mbo
from psdi.mbo import MboRemote 
from psdi.mbo import MboSet
from psdi.mbo import MboValue
from psdi.mbo import MboConstants
from psdi.app.workorder import WO
from psdi.server import MXServer
from java.util import Date

v_quotetype = mbo.getString("CDS_QUOTE_TYPE")
v_tempjpnum = "7DAY"
v_wol1 = mbo.getString("WOL1")
print "Quote Type **********************===>"+str(v_quotetype)
if (v_quotetype == "LIGHT" and v_wol1 == "7DAY"):
	v_tempjpnum = "7DAY"
if (v_quotetype == "FORMAL" and v_wol1 == "30DAY"):
	v_tempjpnum = "30DAY"
if (v_quotetype == "FORMAL" and v_wol1 == "60DAY"):
	v_tempjpnum = "60DAY"		
if (v_quotetype == "FORMAL" and v_wol1 == "60DAYM"):
	v_tempjpnum = "60DAYM"		
mbo.setValue("JPNUM",v_tempjpnum,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
jpset = mbo.getMboSet("$JP","JOBPLAN","jpnum = '"+str(v_tempjpnum)+"' and status = 'ACTIVE'")
estdur = jpset.getMbo(0).getString("CDS_EST_DUR_DAYS")
jprevnum = jpset.getMbo(0).getString("PLUSCREVNUM")
mbo.setValue("CDS_EST_DUR_DAYS",estdur,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
mbo.setValue("PLUSCJPREVNUM",jprevnum,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
jptaskSet = mbo.getMboSet("$JPTASK","JOBTASK","jpnum = '"+str(v_tempjpnum)+"' and pluscjprevnum = (select pluscrevnum from jobplan where jpnum = '"+str(v_tempjpnum)+"' and status = 'ACTIVE')")
woactivityset = mbo.getMboSet("WOACTIVITY")
woactivityset.deleteAll()

if(jptaskSet.moveFirst() is not None):	
	for i in range(0,jptaskSet.count()):
		#print "Inside for ******************************"
		jptaskmbo = jptaskSet.getMbo(i) 
		woact = woactivityset.add()
		woact.setValue("PARENT",mbo.getString("WONUM"))
		woact.setValue("WOSEQUENCE",jptaskmbo.getString("JPTASK"))
		woact.setValue("DESCRIPTION",jptaskmbo.getString("DESCRIPTION"))
		woact.setValue("ESTDUR",jptaskmbo.getString("TASKDURATION"))