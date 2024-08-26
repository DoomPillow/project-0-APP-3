import time

class Condition:
    def __init__(self, name, apply_effect, remove_effect, reapply = False):
        self.name = name
        self.apply_effect = apply_effect
        self.reapply = reapply
        self.remove_effect = remove_effect

    def apply(self, target):
        self.apply_effect(target)

    def remove(self, target):
        self.remove_effect(target)

# Define effects for conditions
def apply_angry(target):
    if "💢" not in target.emojo:
        target.emojo += "💢"
        target.hitratio -= 30
        target.dmgbonus += 3


def remove_angry(target):
    if "💢" in target.emojo:
        target.emojo = target.emojo.replace('💢', '')
        target.hitratio += 30
        target.dmgbonus -= 3


def apply_poisoned(target):
    if "❤️" in target.emojo:
        target.emojo = target.emojo.replace('❤️', '💚')
    else: 
        target.hp -= 2
        print(f"> {target.name} takes 2 poison damage")
        time.sleep(1)


def remove_poisoned(target):
    if "💚" in target.emojo:
        target.emojo = target.emojo.replace('💚', '❤️')


def apply_stunned(target):
    if "💫" not in target.emojo:
        target.emojo += "💫"


def remove_stunned(target):
    if "💫" in target.emojo:
        target.emojo = target.emojo.replace('💫', '')
        print(f"> {target.name} shakes off their daze!!")
        time.sleep(1)

def apply_soapy(target):
    if "🫧" not in target.emojo:
        target.emojo += "🫧"
        target.hitratio -= 25


def remove_soapy(target):
    if "🫧" in target.emojo:
        target.emojo = target.emojo.replace('🫧', '')
        target.hitratio += 25
        print(f"> {target.name} wipes off the suds.")
        time.sleep(1)

# Instantiate conditions
conditions = {
    "angry": Condition("angry", apply_effect=apply_angry, remove_effect=remove_angry),
    "poisoned": Condition("poisoned", apply_effect=apply_poisoned, remove_effect=remove_poisoned, reapply = True),
    "stunned": Condition("stunned", apply_effect=apply_stunned, remove_effect=remove_stunned),
    "soapy": Condition("soapy", apply_effect=apply_soapy, remove_effect=remove_soapy),
}