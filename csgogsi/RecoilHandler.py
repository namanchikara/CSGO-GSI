import pyautogui
import time

class RecoilHandler:
    def __init__(self):
        self.weapon = None

    def update_weapon_if_required(self, weapons):
        active_weapon = self.get_active_weapon(weapons)
        if self.weapon != active_weapon:
            self.weapon = active_weapon
            self.afterUpdate()

    def get_active_weapon(self, weapons):
        for weapon in weapons.values():
            if weapon['state'] == 'active':
                return weapon['name']

    def afterUpdate(self):
        print(self.weapon)
        if self.weapon == 'weapon_ak47':
            self.sendKey("f18")

        elif self.weapon == 'weapon_m4a1':
            self.sendKey("f16")

        elif self.weapon == 'weapon_m4a1_silencer' or self.weapon == 'weapon_galilar' or self.weapon == 'weapon_famas':
            self.sendKey("f17")
        else:
            self.sendKey("num0")

    @staticmethod
    def sendKey(key):
        print("sending key " + key)
        pyautogui.keyDown(key)
        time.sleep(0.05)
        pyautogui.keyUp(key)
