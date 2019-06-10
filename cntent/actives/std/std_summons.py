from cntent.actives.std.callbacks.callbacks import summon_on_target_cell
from cntent.monsters.undead import skeleton

from mechanics.actives import Active, ActiveTags
from battlefield import Cell
from mechanics.actives import Cost

from cntent.actives.conditions.conditions import range_condition, within_angle

summon_skeleton_cb = summon_on_target_cell(skeleton)

summon_skeleton = Active(Cell,
                         [range_condition(1,1.5), within_angle(45)],
                         Cost(stamina=1, health=100, mana=75),
                         callbacks=[summon_skeleton_cb],
                         cooldown=40,
                         tags=[ActiveTags.SUMMON],
                         name="Summon Skeleton",
                         icon="skeleton.png"
                         )