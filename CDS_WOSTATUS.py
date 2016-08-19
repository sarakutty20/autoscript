from psdi.mbo import Mbo
from psdi.mbo import MboRemote
from psdi.mbo import MboValue
from psdi.mbo import MboConstants
from psdi.app.workorder import WO
from psdi.server import MXServer
from java.util import Date
from java.util import Calendar

today=Calendar.getInstance()

#"Complete" tick box set On, status is not COMP yet: change status to COMP; if actual finish blank, populate it with current date
if cds_childcomp == 1 and status <> 'COMP':
  mbo.changeStatus("COMP", MXServer.getMXServer().getDate(), 'Status Automatically changed by script',11L);
  if actfinish is None:
    actfinish = MXServer.getMXServer().getDate()
#if there are brothers next in the sequence, change their status to In Progress
  if mbo.getMboSet("CDS_NEXTSIBLING").count() <> 0 : 
    pwo = mbo.getMboSet("CDS_NEXTSIBLING").getMbo(0)
    pwo.changeStatus("INPRG", today.getTime(), 'Status Automatically changed by script')

#If user sets the "Complete" tick box from On to Off, set status Back In Progress and clear actual finish
#if cds_childcomp == 0 and status == 'COMP':
#  mbo.changeStatus("BACKINPRG", MXServer.getMXServer().getDate(), 'Status Automatically changed by script',11L);
#  actfinish = ""