from abc import ABC, abstractmethod
import v
import weapons

weapon_attachments = []


def get_weapon_attachment_by_name(name):
    for a in weapon_attachments:
        if a.name == name:
            return a
    return None


class weapon_attachment(ABC):
    def __init__(self, name):
        self.name = name
        self.allowed_weapon_sorts = []
        self.allowed_weapon_names = []
        self.needed_resources = {}
        weapon_attachments.append(self)

    @property
    def description(self):
        final = "no description available"
        with open("descriptions.txt", 'r') as f:
            items = f.read().split("\n")
            for i in items:
                if i[0:len(self.name)+1] == self.name+":":
                    return i.replace(self.name+":", "")
        return final

    def has_player_enough_resources(self, inventory, the_weapon):
        for r in self.needed_resources:
            if inventory.get(r) is None:
                return False
            if inventory[r] < self.needed_resources[r]*round(the_weapon.get_tier_formula()):
                return False
        return True

    def remove_resources(self, inventory, the_weapon):
        for r in self.needed_resources:
            inventory[r] -= self.needed_resources[r]*round(the_weapon.get_tier_formula())

    def display_resources_in_text(self, the_weapon):
        results = []
        for r in self.needed_resources:
            results.append(
                str(self.needed_resources[r]*round(the_weapon.get_tier_formula()))+" "+r)
        return v.get_list_in_text(results)

    @abstractmethod
    def attach_to_weapon(self, weapon):
        pass


class small_silencer(weapon_attachment):
    def __init__(self):
        super().__init__("small_silencer")
        self.allowed_weapon_sorts = [
            "sub_machine_gun"]
        self.allowed_weapon_names = ["beretta92A1", "colt_m1911"]
        self.needed_resources = {
            "metal_piece": 2,
            "rubber_piece": 1
        }

    def attach_to_weapon(self, the_weapon):
        the_weapon.silenced = True


class large_silencer(weapon_attachment):
    def __init__(self):
        super().__init__("large_silencer")
        self.allowed_weapon_names = ["dsr50"]
        self.needed_resources = {
            "metal_piece": 2,
            "plastic_piece": 1,
            "rubber_piece": 1
        }

    def attach_to_weapon(self, the_weapon):
        the_weapon.silenced = True


class extended_magazine(weapon_attachment):
    def __init__(self):
        super().__init__("extended_magazine")
        self.allowed_weapon_sorts = [
            "sub_machine_gun", "assault_rifle", "machine_gun","marksman_rifle"]
        self.allowed_weapon_names = []
        self.needed_resources = {
            "metal_piece": 2,
            "plastic_piece": 1
        }

    def attach_to_weapon(self, the_weapon):
        we = weapons.weapon(the_weapon.name)
        the_weapon.max_ammo = we.max_ammo+round(we.max_ammo/4)


class small_barrel(weapon_attachment):
    def __init__(self):
        super().__init__("small_barrel")
        self.allowed_weapon_sorts = [
            "pistol","revolver"]
        self.needed_resources = {
            "metal_piece": 2
        }

    def attach_to_weapon(self, the_weapon):
        we = weapons.weapon(the_weapon.name)
        the_weapon.range = we.range+5


class large_barrel(weapon_attachment):
    def __init__(self):
        super().__init__("large_barrel")
        self.allowed_weapon_sorts = [
            "machine_gun","marksman_rifle"]
        self.needed_resources = {
            "metal_piece": 3
        }

    def attach_to_weapon(self, the_weapon):
        we = weapons.weapon(the_weapon.name)
        the_weapon.range = we.range+10

class stock(weapon_attachment):
    def __init__(self):
        super().__init__("stock")
        self.allowed_weapon_sorts = [
            "machine_gun", "assault_rifle"]
        self.needed_resources = {
            "plastic_piece": 2,
            "rubber_piece": 1,
        }

    def attach_to_weapon(self, the_weapon):
        pass

class choke_tube(weapon_attachment):
    def __init__(self):
        super().__init__("choke_tube")
        self.allowed_weapon_sorts = [
            "shotgun"]
        self.needed_resources = {
            "metal_piece": 2,
            "rubber_piece": 1,
        }

    def attach_to_weapon(self, the_weapon):
        the_weapon.spread+=1

class precision_barrel(weapon_attachment):
    def __init__(self):
        super().__init__("precision_barrel")
        self.allowed_weapon_sorts = [
            "sniper_rifle"]
        self.needed_resources = {
            "metal_piece": 4
        }

    def attach_to_weapon(self, the_weapon):
        we = weapons.weapon(the_weapon.name)
        the_weapon.range = we.range+25

class large_scope(weapon_attachment):
    def __init__(self):
        super().__init__("large_scope")
        self.allowed_weapon_sorts = [
            "marksman_rifle"]
        self.allowed_weapon_names = []
        self.needed_resources = {
            "metal_piece": 2,
            "glass_piece": 1
        }

    def attach_to_weapon(self, the_weapon):
        the_weapon.scope = True



attachment1 = extended_magazine()
attachment2 = small_silencer()
attachment3 = large_silencer()
attachment4 = large_barrel()
attachment5 = small_barrel()
attachment6 = stock()
attachment7 = choke_tube()
attachment8 = precision_barrel()
attachment9 = large_scope()
