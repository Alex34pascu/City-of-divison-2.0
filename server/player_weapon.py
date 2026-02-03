import v
import weapon_attachment
import weapons


class player_weapon(weapons.weapon):
    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "modifications": [],
            "loaded_ammo": [0],
            "jammed": [False],
            "degradation": [0],
            "silenced": [False],
            "scope": [False],
        }

    @property
    def degradation(self):
        return self.data["degradation"][0]

    @degradation.setter
    def degradation(self, value):
        self.data["degradation"][0] = value

    @property
    def loaded_ammo(self):
        return self.data["loaded_ammo"][0]

    @loaded_ammo.setter
    def loaded_ammo(self, value):
        self.data["loaded_ammo"][0] = value

    @property
    def modifications(self):
        return self.data["modifications"]

    @modifications.setter
    def modifications(self, value):
        self.data["modifications"] = value

    @property
    def jammed(self):
        return self.data["jammed"][0]

    @jammed.setter
    def jammed(self, value):
        self.data["jammed"][0] = value

    @property
    def silenced(self):
        return self.data["silenced"][0]

    @silenced.setter
    def silenced(self, value):
        self.data["silenced"][0] = value

    @property
    def scope(self):
        return self.data["scope"][0]

    @scope.setter
    def scope(self, value):
        self.data["scope"][0] = value



    def get_upgrades(self):
        final = []
        for w in weapon_attachment.weapon_attachments:
            if self.sort in w.allowed_weapon_sorts or self.name in w.allowed_weapon_names:
                final.append(
                    w.name+": requires "+w.display_resources_in_text(self)+". Description: "+w.description)
        if self.jammed == True:
            final.append("jam clear this weapon")
        return final

    @property
    def is_degradated(self):
        if self.degradation>=100:
            return True
        return False

    def get_info(self):
        jam_messages = {
            False: "not jammed",
            True: "jammed"}
        modifications_string = v.get_list_in_text(self.modifications)
        if modifications_string == "":
            modifications_string = "no attachments"
        else:
            modifications_string = "a "+modifications_string+" attached"
        degradation_text = ""
        if self.sort != "melee":
            if self.is_degradated:
                degradation_text = ". This weapon is degraded"
            else:
                degradation_text = ". This weapon is " + \
                    str(self.degradation)+"% degraded"
        jam_text=""
        if self.sort!="melee":
             jam_text="This "+self.name+" is " + \
            jam_messages[self.jammed]+". "
        else:
            jam_text="a "+self.name+" can't be jammed. "
        final = jam_text+"It has " + \
                modifications_string+degradation_text
        return final

    def use_attachments(self):
        for m in self.modifications:
            attachment = weapon_attachment.get_weapon_attachment_by_name(m)
            attachment.attach_to_weapon(self)

    def load(self, data):
        for o in data:
            if o != "name":
                self.data[o] = data[o]
        self.use_attachments()
