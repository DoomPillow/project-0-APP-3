import items as itm
from conditions import conditions

##### Player Class
class Player:
    def __init__(self):
        self.emojo = "❤️"
        self.name = "You"
        self.hpmax = 25
        self.hp = self.hpmax
        self.ppmax = 50
        self.pp = self.ppmax
        self.active_conditions = {}
        self.inventory = [
            itm.burger(),
            itm.bandaid(), 
            itm.juice()
        ]

        self.target = None

        self.dmgbonus = 0
        #self.hitratio = 90 # % chance of hitting. currently doesn't do anything for the player

    # Gives player buffs/debuffs
    def apply_condition(self, condition, duration):
        if condition.name in self.active_conditions:
            self.active_conditions[condition.name] += duration
        else:
            self.active_conditions[condition.name] = duration
            condition.apply(self)

    # Manages active player buffs/debuffs
    def rebuff(self):

        ## Remove conditions with expired cooldowns
        expired_conditions = []

        for condition_name, duration in self.active_conditions.items():
            self.active_conditions[condition_name] = max(duration - 1, 0)
            
            if self.active_conditions[condition_name] <= 0:
                expired_conditions.append(condition_name)
            
            # If condition is not expired, apply its effects
            elif conditions[condition_name].reapply:
                conditions[condition_name].apply(self)
                

        for condition_name in expired_conditions:
            condition = conditions[condition_name]
            condition.remove(self)
            del self.active_conditions[condition_name]

    def has_condition(self, condition_name):
        return self.active_conditions.get(condition_name, 0) > 0

## Shouldn't be initialized in this file, but is here for now
player = Player()