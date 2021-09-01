#!/usr/bin/env python

from state.IState import IState
import state
from db.EquipmentRecord import EquipmentRecord
from db.AccountRecord import AccountRecord


class Enquiry():
    Invalid = ""
    Borrow = "1"
    Return = "2"
    Update = "3"


class CommonResource():
    user: EquipmentRecord = None
    equipment:AccountRecord = None
    prev_state:IState = None

    @staticmethod
    def initialize():
        CommonResource.user = AccountRecord()
        CommonResource.equipment = EquipmentRecord()
        CommonResource.prev_state = state.Init()
