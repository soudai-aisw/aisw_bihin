#!/usr/bin/env python

if __name__ == "__main__":
    import os
    import sys
    import time
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.EquipmentRecord import EquipmentRecord
from db.EquipmentLedger import EquipmentLedger
import state as state
import dev.display.Console as Console
import dev.input as input
from db.UserProcedure import UserProcedure
from state.commonResource import CommonResource as cmn_res
import config

class StandbyAppendEquipmentIdRead(state.IState):
    def entry(self):
        if config.is_debug_mode():
            self.__input = input.SunitizedString(
                input.UserInputReader()
            )
        else:
            self.__input = input.SunitizedString(
                input.RFIDReader()
            )

        self.__get_next_state = state.ErrorHasOccurred()
        Console.clear()
        Console.puts("関連付けるRFIDをかざしてください")
        Console.puts(">", end="")

    def do(self):
        self.__input.capture()

    def exit(self):
        equipment_rfid = self.__input.get_string()

        record = UserProcedure().get_equipment_record_by(rfid=equipment_rfid)

        if record is None:
            #登録処理
            cmn_res.equipment.data[EquipmentRecord.RFID] = equipment_rfid
            self.__get_next_state = state.ConfirmToAppendNewEquipment()

        else:
            cmn_res.equipment.data = record
            Console.puts("このRFIDは既に",cmn_res.equipment.data[EquipmentRecord.EQUIPMENT_ID],"と関連付けられています。", "\n")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください")
            self.__get_next_state = state.ErrorHasOccurred()
 
    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()

