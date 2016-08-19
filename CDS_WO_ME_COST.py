#   Description:
#   CDS_WO_ME_COST.py
#   Script to total the costs for the manufacture process
#
#   Subversion Info
#   ---------------
#   $Id$
#
#
#   Revision History
#   ----------------
#   Created:    02/02/2016
#   --------------------------------------------------------------------------
#   Version Description                             CMS Ref         Changed By
#   -------+---------------------------------------+---------------+----------
#   1.0      Initial version                        N/A             W Mahmud
#   1.1		 Modified relatioship to sum recurring					Saravanan
#			 and non recurring cost 
#    
#   Launch Point Variables
#   ----------------------
#   Various attribute launch points
#
#   Relationships
#   -------------
#
from psdi.mbo import Mbo

# Updates totals in real-time

# Initialise value
# Lead
me_total_lead_nrec = 0
rfq_lead1 = 0
rfq_lead2 = 0
rfq_lead3 = 0
rfq_lead4 = 0

total_lead_rec = 0
child_lead1 = 0
child_lead2 = 0
child_lead3 = 0
child_lead4 = 0

# Cost
me_total_cost_nrec = 0
rfq_cost1 = 0
rfq_cost2 = 0
rfq_cost3 = 0
rfq_cost4 = 0

total_cost_rec = 0
child_cost1 = 0
child_cost2 = 0
child_cost3 = 0
child_cost4 = 0

# Non-recurring costs CDS_WO_MAN_NREC_COST,CDS_WO_MAN_REC_COST
# From ME process

nonrecmboset = mbo.getMboSet("CDS_WO_MAN_NREC_COST")
if nonrecmboset:
    me_total_lead_nrec = nonrecmboset.sum("LEADTIME")
    me_total_cost_nrec = nonrecmboset.sum("COST")
	
#me_total_lead_nrec = mbo.getInt("CDS_MECAPCTYLEADTIME") + mbo.getInt("CDS_TRNPLANLEAD") + mbo.getInt("CDS_FAIRLEADTIME") + mbo.getInt("CDS_PKGNGLEADTIME")
mbo.setValue("CDS_LEADTIME_QTY_1_NREC", me_total_lead_nrec)
mbo.setValue("CDS_LEADTIME_QTY_2_NREC", me_total_lead_nrec)
mbo.setValue("CDS_LEADTIME_QTY_3_NREC", me_total_lead_nrec)
mbo.setValue("CDS_LEADTIME_QTY_4_NREC", me_total_lead_nrec)

#me_total_cost_nrec = mbo.getFloat("CDS_ADDTNALMANHRS") + mbo.getFloat("CDS_ADDNTMEHRS")
mbo.setValue("CDS_COST_QTY_1_NREC", me_total_cost_nrec)
mbo.setValue("CDS_COST_QTY_2_NREC", me_total_cost_nrec)
mbo.setValue("CDS_COST_QTY_3_NREC", me_total_cost_nrec)
mbo.setValue("CDS_COST_QTY_4_NREC", me_total_cost_nrec)

# Recurring costs
# From ME process 
recMboSet = mbo.getMboSet("CDS_WO_MAN_REC_COST")
if recMboSet:
    total_lead_rec = recMboSet.sum("LEADTIME")
    total_cost_rec = recMboSet.sum("COST")
# Set totals        
mbo.setValue("CDS_LEADTIME_QTY_1_REC",total_lead_rec)
mbo.setValue("CDS_LEADTIME_QTY_2_REC",total_lead_rec)
mbo.setValue("CDS_LEADTIME_QTY_3_REC",total_lead_rec)
mbo.setValue("CDS_LEADTIME_QTY_4_REC",total_lead_rec)
mbo.setValue("CDS_COST_QTY_1_REC",total_cost_rec)
mbo.setValue("CDS_COST_QTY_2_REC",total_cost_rec)
mbo.setValue("CDS_COST_QTY_3_REC",total_cost_rec)
mbo.setValue("CDS_COST_QTY_4_REC",total_cost_rec)

# RFQ/DLF etc values
rfq_lead1 = mbo.getInt("CDS_QUOTE_LEADTIME_QTY_1")
rfq_cost1 = mbo.getFloat("CDS_QUOTE_QTY_1")
rfq_lead2 = mbo.getInt("CDS_QUOTE_LEADTIME_QTY_2")
rfq_cost2 = mbo.getFloat("CDS_QUOTE_QTY_2")
rfq_lead3 = mbo.getInt("CDS_QUOTE_LEADTIME_QTY_3")
rfq_cost3 = mbo.getFloat("CDS_QUOTE_QTY_3")
rfq_lead4 = mbo.getInt("CDS_QUOTE_LEADTIME_QTY_4")
rfq_cost4 = mbo.getFloat("CDS_QUOTE_QTY_4")

# Generate totals from children workorders
childMboSet = mbo.getMboSet("CDS_SHOWCHILDREN_ORDITEM")
if childMboSet:
    child_lead1 = childMboSet.sum("CDS_LEADTIME_QTY_1")
    child_lead2 = childMboSet.sum("CDS_LEADTIME_QTY_2")
    child_lead3 = childMboSet.sum("CDS_LEADTIME_QTY_3")
    child_lead4 = childMboSet.sum("CDS_LEADTIME_QTY_4")
    child_cost1 = childMboSet.sum("CDS_COST_GROSS_QTY_1")
    child_cost2 = childMboSet.sum("CDS_COST_GROSS_QTY_2")
    child_cost3 = childMboSet.sum("CDS_COST_GROSS_QTY_3")
    child_cost4 = childMboSet.sum("CDS_COST_GROSS_QTY_4")

mbo.setValue("CDS_LEADTIME_QTY_1_CHILDREN",child_lead1)
mbo.setValue("CDS_LEADTIME_QTY_2_CHILDREN",child_lead2)
mbo.setValue("CDS_LEADTIME_QTY_3_CHILDREN",child_lead3)
mbo.setValue("CDS_LEADTIME_QTY_4_CHILDREN",child_lead4)
mbo.setValue("CDS_COST_QTY_1_CHILDREN",child_cost1)
mbo.setValue("CDS_COST_QTY_2_CHILDREN",child_cost2)
mbo.setValue("CDS_COST_QTY_3_CHILDREN",child_cost3)
mbo.setValue("CDS_COST_QTY_4_CHILDREN",child_cost4)

    
# Gross Totals
# Set totals
mbo.setValue("CDS_LEADTIME_QTY_1",mbo.getInt("CDS_LEADTIME_QTY_1_NREC")+mbo.getInt("CDS_LEADTIME_QTY_1_REC")+rfq_lead1+mbo.getInt("CDS_LEADTIME_QTY_1_CHILDREN"))
mbo.setValue("CDS_LEADTIME_QTY_2",mbo.getInt("CDS_LEADTIME_QTY_2_NREC")+mbo.getInt("CDS_LEADTIME_QTY_2_REC")+rfq_lead2+mbo.getInt("CDS_LEADTIME_QTY_2_CHILDREN"))
mbo.setValue("CDS_LEADTIME_QTY_3",mbo.getInt("CDS_LEADTIME_QTY_3_NREC")+mbo.getInt("CDS_LEADTIME_QTY_3_REC")+rfq_lead3+mbo.getInt("CDS_LEADTIME_QTY_3_CHILDREN"))
mbo.setValue("CDS_LEADTIME_QTY_4",mbo.getInt("CDS_LEADTIME_QTY_4_NREC")+mbo.getInt("CDS_LEADTIME_QTY_4_REC")+rfq_lead4+mbo.getInt("CDS_LEADTIME_QTY_4_CHILDREN"))
mbo.setValue("CDS_COST_GROSS_QTY_1",mbo.getFloat("CDS_COST_QTY_1_NREC")+mbo.getFloat("CDS_COST_QTY_1_REC")+rfq_cost1+mbo.getFloat("CDS_COST_QTY_1_CHILDREN"))
mbo.setValue("CDS_COST_GROSS_QTY_2",mbo.getFloat("CDS_COST_QTY_2_NREC")+mbo.getFloat("CDS_COST_QTY_2_REC")+rfq_cost2+mbo.getFloat("CDS_COST_QTY_2_CHILDREN"))
mbo.setValue("CDS_COST_GROSS_QTY_3",mbo.getFloat("CDS_COST_QTY_3_NREC")+mbo.getFloat("CDS_COST_QTY_3_REC")+rfq_cost3+mbo.getFloat("CDS_COST_QTY_3_CHILDREN"))
mbo.setValue("CDS_COST_GROSS_QTY_4",mbo.getFloat("CDS_COST_QTY_4_NREC")+mbo.getFloat("CDS_COST_QTY_4_REC")+rfq_cost4+mbo.getFloat("CDS_COST_QTY_4_CHILDREN"))

mbo.getThisMboSet().save()