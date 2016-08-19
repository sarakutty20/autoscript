from psdi.mbo import Mbo
from psdi.mbo import MboSet

pcat = mbo.getMboSet("CDS_PART_CAT_P")
scat = mbo.getMboSet("CDS_PART_CAT_S")
vcs = mbo.getMboSet("CDS_VCS")
dlf = mbo.getMboSet("CDS_DLF")

if pcat.count() != 0 or scat.count() != 0:
    mbo.setValue("IS_CATALOGUE", 1)

if vcs.count() != 0:
    mbo.setValue("IS_VCS", 1)

if dlf.count() != 0:
    mbo.setValue("IS_DLF", 1)