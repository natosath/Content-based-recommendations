"""from code.merge import filter_basics as fb
from code.merge import improved_merge_basics_ratings as mbr
from code.merge import improved_merge_basics_ratings as mmc
from code.merge import adjust_final as af"""

from code.merge import adjust_final as af
from code.merge import improved_merge_basics_ratings as mbr
from code.merge import improved_merge_merged_crew as mmc

# fb.filter_basics()
mbr.main_mbr()
mmc.main_mmc()
af.main_adjust()
