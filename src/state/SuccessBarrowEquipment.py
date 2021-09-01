#!/usr/bin/env python
if __name__ == "__main__":
    import os
    import sys
#   sys.path.append('../')
#    sys.path.append('../../')
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db.EquipmentRecord import EquipmentRecord
from db.AccountRecord import AccountRecord
import state as state
import dev.display.Console as Console
from state.commonResource import CommonResource as cmn_res


class SuccessBarrowEquipment(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("ユーザID  ：", cmn_res.user.data[AccountRecord.EMPLOYEE_ID])
        Console.puts("機材ID    ：", cmn_res.equipment.data[EquipmentRecord.EQUIPMENT_ID])
        Console.puts("機材名    ：", cmn_res.equipment.data[EquipmentRecord.EQUIPMENT_NAME])
        Console.puts("返却予定日：", cmn_res.equipment.data[EquipmentRecord.END_DATE], "\n")
        Console.puts("上記の情報で備品の貸出手続きが完了しました。\n")
        Console.puts("続けて他の機器の貸出処理が実施できます。")
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        pass

    def exit(self):
        self.__get_next_state = state.GotoNextAfterWaiting()
        # 連続で貸出処理を行うためID入力へ遷移
        self.__get_next_state.set_next_state(
            state.StandbyBarrowEquipmentIdRead())

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return True

# -----------------------------------------------------------------------------


def debug_this_module():
    Console.clear()
    temp = SuccessBarrowEquipment()

    temp.entry()

    while True:
        temp.do()
        if (temp.should_exit()):
            temp.exit()
            break


if __name__ == "__main__":
    help(debug_this_module)
    state.CommonResource.employeeId = "0079049"
    state.CommonResource.equipmentId = "00-00-00-00"
    state.CommonResource.expirationDate = "21/07/15"
    debug_this_module()
