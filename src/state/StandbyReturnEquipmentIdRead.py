#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input
from db.UserProcedure import UserProcedure
from state.commonResource import CommonResource as cmn_res
from db.EquipmentRecord import EquipmentRecord
import config

class StandbyReturnEquipmentIdRead(state.IState):
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
        Console.puts("返却する備品のRFIDをかざしてください")
        Console.puts(">", end="")

    def do(self):
        self.__input.capture()

    def exit(self):
        equipment_rfid = self.__input.get_string()

        status = UserProcedure().get_equipment_status_by(rfid=equipment_rfid)

        # かざされたRFIDがDB照合結果、貸し出されているものだった場合(今は仮値)
        if status == UserProcedure.EquipmentStatus.ALREADY_RESERVED:
            cmn_res.equipment.data = UserProcedure().get_equipment_record_by(rfid=equipment_rfid)

            if UserProcedure(True).return_equipment(equipment_rfid) == True:
                self.__get_next_state = state.SuccessReturnEquipment()
            else:
                Console.puts("返却処理に失敗しました")
                Console.puts("再度試しても失敗する場合、システム管理者に問い合わせください", "\n")
                self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDがDB上貸し出されていない場合
        if status == UserProcedure.EquipmentStatus.AVAILABLE:
            Console.puts("貸し出されていない備品です。")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください", "\n")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDがDB上登録されていない場合
        if status == UserProcedure.EquipmentStatus.NOT_EXIST:
            Console.puts("登録されていない備品です。")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください", "\n")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDが故障中の場合
        if status == UserProcedure.EquipmentStatus.OUT_OF_ORDER:
            Console.puts("故障中につき貸し出し対象外の備品です。")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください", "\n")
            self.__get_next_state = state.ErrorHasOccurred()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()


def debug_this_module():
    temp = StandbyReturnEquipmentIdRead()
    temp.entry()
    time.sleep(0.010)
    if (temp.should_exit()):
        temp.exit()
        print(temp.get_next_state())


if __name__ == "__main__":
    # helpのことはわかっていない
    help(debug_this_module)
    time.sleep(1)
    debug_this_module()
