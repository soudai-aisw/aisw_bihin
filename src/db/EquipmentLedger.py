from db.EquipmentRecord import EquipmentRecord
from db import Ledger
import config


class EquipmentLedger(Ledger):
    @property
    def _db_path(self):
        return config.get_equipment_db_path()

    @property
    def _encoding(self):
        return "shift-jis"

    @property
    def _primary_key(self):
        return EquipmentRecord.EQUIPMENT_ID

    @property
    def _acceptable_object(self):
        return EquipmentRecord