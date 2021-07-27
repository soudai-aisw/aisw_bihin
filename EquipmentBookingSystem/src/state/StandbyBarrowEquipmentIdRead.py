#!/usr/bin/env python

if __name__ == "__main__":
    import os
    import sys
    import time
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import state as state
import dev.display.Console as Console
import dev.input as input
import db.matching.DBmatching as db

class StandbyBarrowEquipmentIdRead(state.IState):
    def entry(self):
        self.__input = input.UserInputReader()
        self.__get_next_state = state.ErrorHasOccurred()
        Console.clear()
        Console.puts("借用する備品のRFIDをかざしてください")
        Console.puts(">", end="")

    def do(self):
        self.__input.capture()

    def exit(self):
        equipmentId = self.__input.get_string()

        #-----DBの戻り値-----
        # 0: 未登録
        # 1：借用可能
        # 2：借用中
        # 3：故障中
        #--------------------

        rfid_return = db.DBmatching_EquIDtoEquStatus(equipmentId)

        # かざされたRFIDがDB照合結果、貸し出されているものでなく登録されているものだった場合
        if rfid_return == 1:
            state.CommonResource.equipmentId = equipmentId
            self.__get_next_state = state.StandbyExpirationDateInputWhenBarrow()

        # かざされたRFIDがDB上貸し出されている場合
        if rfid_return == 2:
            Console.puts("貸し出されている備品です。","\n")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDがDB上登録されていない場合
        if rfid_return == 0:
            Console.puts("登録されていない備品です。","\n")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDが故障中の場合(今は仮値)
        if rfid_return == 3:
            Console.puts("故障中につき貸し出し対象外の備品です。")
            Console.puts("認識と異なる場合は、システム管理者に問い合わせください","\n")
            self.__get_next_state = state.ErrorHasOccurred()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()

def debug_this_module():
    temp = StandbyBarrowEquipmentIdRead()
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

