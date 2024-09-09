import time

class Condition:
    def __init__(self, name, apply_effect, remove_effect, reapply = False):
        self.name = name
        self.apply_effect = apply_effect
        self.reapply = reapply
        self.remove_effect = remove_effect

    def apply(self, target):
        self.apply_effect(target)

    def remove(self, target, output):
        self.remove_effect(target, output)

# Define effects for conditions
def apply_angry(target):
    if "💢" not in target.emojo:
        target.emojo += "💢"
        target.hitratio -= 30
        target.dmgbonus += 3


def remove_angry(target, output):
    if "💢" in target.emojo:
        target.emojo = target.emojo.replace('💢', '')
        target.hitratio += 30
        target.dmgbonus -= 3


def apply_poisoned(target):
    if "❤️" in target.emojo:
        target.emojo = target.emojo.replace('❤️', '💚')
    else: 
        target.hp -= 2
        print(f"> 🟢 {target.name} takes 2 poison damage")
        time.sleep(0.8)


def remove_poisoned(target, output):
    if "💚" in target.emojo:
        target.emojo = target.emojo.replace('💚', '❤️')
    if output:
        print(f"> {target.name} is no longer poisoned!")
        time.sleep(1)


def apply_fire(target):
    if "🔥" not in target.emojo:
        target.emojo += "🔥"
    else:
        target.hp -= 1
        print(f"> 🔥 {target.name} takes 1 damage from the fire!")
        time.sleep(0.8)


def remove_fire(target, output):
    if "🔥" in target.emojo:
        target.emojo = target.emojo.replace('🔥', '')
        if output:
            print(f"> {target.name} is no longer on fire!")
            time.sleep(1)


def apply_stunned(target):
    if "💫" not in target.emojo:
        target.emojo += "💫"


def remove_stunned(target, output):
    if "💫" in target.emojo:
        target.emojo = target.emojo.replace('💫', '')
        if output:
            print(f"> {target.name} shakes off their daze!!")
            time.sleep(1)

def apply_soapy(target):
    if "🫧" not in target.emojo:
        target.emojo += "🫧"
        target.hitratio -= 25


def remove_soapy(target, output):
    if "🫧" in target.emojo:
        target.emojo = target.emojo.replace('🫧', '')
        target.hitratio += 25
        if output:
            print(f"> {target.name} wipes off the suds.")
            time.sleep(1)

def apply_blocking(target):
    if "🛡️" not in target.emojo:
        target.emojo += "🛡️"


def remove_blocking(target, output):
    if "🛡️" in target.emojo:
        target.emojo = target.emojo.replace('🛡️', '')

# Instantiate conditions
conditions = {
    "angry": Condition("angry", apply_effect=apply_angry, remove_effect=remove_angry),
    "poisoned": Condition("poisoned", apply_effect=apply_poisoned, remove_effect=remove_poisoned, reapply = True),
    "fire": Condition("fire", apply_effect=apply_fire, remove_effect=remove_fire, reapply = True),
    "stunned": Condition("stunned", apply_effect=apply_stunned, remove_effect=remove_stunned),
    "soapy": Condition("soapy", apply_effect=apply_soapy, remove_effect=remove_soapy),
    "blocking": Condition("blocking", apply_effect=apply_blocking, remove_effect=remove_blocking),
}