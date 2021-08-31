#!/usr/bin/env python

from datetime import datetime
from db.AccountLedger import AccountLedger
from db.AccountRecord import AccountRecord
from db.EquipmentLedger import EquipmentLedger
from db.EquipmentRecord import EquipmentRecord
from enum import Enum, auto

class UserProcedure:
    class EquipmentStatus(Enum):
        NOT_EXIST = auto()
        OUT_OF_ORDER = auto()
        ALREADY_RESERVED = auto()
        AVAILABLE = auto()

    def __init__(self):
        self.account_ledger = AccountLedger()
        self.equipment_ledger = EquipmentLedger()

    def get_user_record_by(self, rfid=None, employee_id=None):
        if rfid is not None:
            records = self.account_ledger.find_by(AccountRecord.RFID, rfid)
        elif employee_id is not None:
            records = self.account_ledger.find_by(AccountRecord.EMPLOYEE_ID, employee_id)
        else:
            raise SystemError("Invalid arguments.")

        if len(records) == 0:
            return None
        elif len(records) == 1:
            return records.iloc[0]
        else:
            raise SystemError("There are multiple primary keys.")

    def get_equipment_record_by(self, rfid=None, equipment_id=None):
        if rfid is not None:
            records = EquipmentLedger().find_by(
                EquipmentRecord.RFID, rfid)
        elif equipment_id is not None:
            records = EquipmentLedger().find_by(
                EquipmentRecord.EQUIPMENT_ID, equipment_id)
        else:
            raise SystemError("Invalid arguments.")

        if len(records) == 0:
            return None
        elif len(records) == 1:
            return records.iloc[0]
        else:
            raise SystemError("There are multiple primary keys.")

    def get_equipment_status_by(self, rfid=None, equipment_id=None):
        if rfid is not None:
            records = EquipmentLedger().find_by(
                EquipmentRecord.RFID, rfid)
        elif equipment_id is not None:
            records = EquipmentLedger().find_by(
                EquipmentRecord.EQUIPMENT_ID, equipment_id)
        else:
            raise SystemError("Invalid arguments.")

        if len(records) == 0:
            return UserProcedure.EquipmentStatus.NOT_EXIST
        elif len(records) == 1:
            status_dict = {
                "借用可能": UserProcedure.EquipmentStatus.AVAILABLE,
                "借用中": UserProcedure.EquipmentStatus.ALREADY_RESERVED,
                "故障中": UserProcedure.EquipmentStatus.OUT_OF_ORDER
            }
            status = records.iloc[0][EquipmentRecord.STATUS]
            if status in status_dict:
                return status_dict[status]
            else:
                raise SystemError(EquipmentRecord.STATUS, " is out of range.")
        else:
            raise SystemError("There are multiple primary keys.")

    def borrow_equipment(self, user_id, rfid_of_equipment, end_date):
        records = self.equipment_ledger.find_by(
            EquipmentRecord.RFID, rfid_of_equipment)
        if len(records) == 0:
            return False
        elif len(records) == 1:
            record = EquipmentRecord()
            record.data = records.iloc[0]
            record.data = {
                EquipmentRecord.USER_ID: user_id,
                EquipmentRecord.BEGIN_DATE: datetime.now().strftime('%Y/%m/%d'),
                EquipmentRecord.END_DATE: end_date,
                EquipmentRecord.STATUS: "借用中"
            }
            self.equipment_ledger.update(record)
        else:
            raise SystemError("There are multiple primary keys.")
        return True

    def return_equipment(self, rfid_of_equipment):
        records = self.equipment_ledger.find_by(
            EquipmentRecord.RFID, rfid_of_equipment)

        if len(records) == 0:
            return False
        elif len(records) == 1:
            record = EquipmentRecord()
            record.data = records.iloc[0]
            record.data = {
                EquipmentRecord.USER_ID: "-",
                EquipmentRecord.BEGIN_DATE: "-",
                EquipmentRecord.END_DATE: "-",
                EquipmentRecord.STATUS: "借用可能"
            }
            self.equipment_ledger.update(record)
        else:
            raise SystemError("There are multiple primary keys.")
        return True

    def update_equipment_return_date(self, user_id, id_of_equipment, end_date):
        records = self.equipment_ledger.find_by(
            EquipmentRecord.EQUIPMENT_ID, id_of_equipment)

        if len(records) == 0:
            return False
        elif len(records) == 1:
            record = EquipmentRecord()
            record.data = records.iloc[0]
            record.data = {
                EquipmentRecord.USER_ID: user_id,
                EquipmentRecord.END_DATE: end_date
            }
            self.equipment_ledger.update(record)
        else:
            raise SystemError("There are multiple primary keys.")
        return True
