from dataclasses import dataclass

@dataclass
class Card:
    context: str
    card_id: int
    card_mda_type: str
    admin_state: str = None
    def __post_init__(self):
        if not isinstance(self.card_id, int):
            self.card_id = int(self.card_id)

@dataclass
class Mda:
    context: str
    card_id: int
    subcard_id: int
    card_mda_type: str
    xiom_id: str = None
    admin_state: str = None
    def __post_init__(self):
        for field_name in ["card_id", "subcard_id"]:
            value = getattr(self, field_name)
            if isinstance(value, str) and value.isdigit():
                setattr(self, field_name, int(value))	

@dataclass
class Xiom:
    context: str
    card_id: int
    xiom_id: str
    card_mda_type: str
    admin_state: str = None
    def __post_init__(self):
        if not isinstance(self.card_id, int):
            self.card_id = int(self.card_id)

@dataclass
class Fp:
    context: str
    card_id: int
    subcard_id: int
    ingress_network_slope_policy: str = None
    ingress_network_queue_policy: str = None	
    fp_dist_cpu_dynamic_policer_pool: str = None
    admin_state: str = None
    def __post_init__(self):
        for field_name in ["card_id", "subcard_id"]:
            value = getattr(self, field_name)
            if isinstance(value, str) and value.isdigit():
                setattr(self, field_name, int(value))

@dataclass
class Sfm:
    context: str
    card_id: int
    card_mda_type: str
    admin_state: str = None
    def __post_init__(self):
        if not isinstance(self.card_id, int):
            self.card_id = int(self.card_id)
