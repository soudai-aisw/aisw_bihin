#!/usr/bin/env python
if __name__ == "__main__":
    import os
    import sys
#   sys.path.append('../')
#    sys.path.append('../../')
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time
import state as state
import dev.display.Console as Console
import dev.input as input

class SuccessUpdateEquipment(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("ユーザID  ：",state.CommonResource.employeeId)
        Console.puts("機材ID    ：",state.CommonResource.equipmentId)
        Console.puts("返却予定日：",state.CommonResource.expirationDate,"\n")

        Console.puts("上記の情報で備品の更新手続きが完了しました。")

        self.__start_time = time.time()
        self.__pressed_key = input.PressedKey()

    def do(self):
        self.__pressed_key.capture()

    def exit(self):
        pass

    def get_next_state(self):
        Console.clear()
        Console.puts("続けて他の機器の更新処理が実施できます。")
        # 連続で更新処理を行うためID入力へ遷移
        return state.StandbyUpdateEquipmentIdInput()

    def should_exit(self):
        #何か押されたら Or 3sで飛ぶ
        return self.__pressed_key.exists() or self.__timeout_detected()
 
    # 3秒経過でタイムアウト
    def __timeout_detected(self):
        elapsed_time = time.time() - self.__start_time
        return (3 < elapsed_time)

#-----------------------------------------------------------------------------
def debug_this_module():
    Console.clear()
    temp = SuccessUpdateEquipment()

    temp.entry()
    time.sleep(0.010)

    while True:
        time.sleep(0.010)

        temp.do()
        if (temp.should_exit()):
            temp.exit()
            break

if __name__ == "__main__":
    help(debug_this_module)
    state.CommonResource.employeeId = "0079049"
    state.CommonResource.equipmentId = "00-00-00-00"
    state.CommonResource.expirationDate = "21/07/15"
    time.sleep(1)
    debug_this_module()
