from psdi.mbo import Mbo
from psdi.mbo import MboRemote 
from psdi.mbo import MboValue
from psdi.mbo import MboConstants
from java.util import Date
from java.util import Calendar

today=Calendar.getInstance()

#for workscopes: if target start is modified, set the first children milestone's target start
if worktype == 'WKSCP' and targcompdate_modified == True and targcompdate is not None:
  cfm_targstartdate = today.getTime()

#for milestones:
if istask:

#if target complete is modified and target start is not, set the next milestone's target start
  if targcompdate_modified == True and targstartdate_modified == False and targcompdate is not None:
    if snm_estdur is not None:
      snm_targstartdate = targcompdate
  
  if targstartdate_modified == True and targstartdate is not None and estdur is not None:
    targcompdate = Date(targstartdate.getTime() + long (estdur * 60 * 60 * 1000))
    if snm_estdur is not None:
      snm_targstartdate = targcompdate

  if status_modified and status == 'INPRG':
    targcompdate = today.getTime()
    targstartdate = targcompdate
    targcompdate = Date(targstartdate.getTime() + long (estdur * 60 * 60 * 1000))
    if snm_targstartdate is not None:
      snm_targstartdate = targcompdate