#!/usr/bin/env python

if __name__ == "__main__":
    import time
    import sys
    sys.path.append('../')
    sys.path.append('../../')

import time
import state as state
import dev.display.Console as Console
import dev.input as input


class SuccessReturnEquipment(state.IState):
    def entry(self):
        Console.puts("上記の情報で備品の返却手続きが完了しました。")
        self.__submitted = False
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        # 1s間、entryで表示した画面で固定する
        time.sleep(1.000)
        self.__submitted = True

    def exit(self):
        # 無条件で返却備品RFIDかざす状態へ遷移
        self.__get_next_state = state.StandbyReturnEquipmentIdRead()

    def get_next_state(self):
            return self.__get_next_state

    def should_exit(self):
            return self.__submitted

def debug_this_module():
    Console.clear()
    temp = SuccessReturnEquipment()

    temp.entry()
    time.sleep(0.010)

    while True:
        time.sleep(0.010)
        temp2.capture()
        temp.do()
        if (temp.should_exit()):
            temp.exit()
            break

if __name__ == "__main__":
    help(debug_this_module)
    time.sleep(1)
    debug_this_module()