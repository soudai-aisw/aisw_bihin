#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input

class StandbyUpdateEquipmentIdInput(state.IState):
    def entry(self):
        Console.puts("更新する機材のIDをキーボードで入力してください")
        Console.puts(">",end="")
        self.__input = input.UserInputReader()
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        # キーボード入力受付（Enterが押されたらexitへ移行する）
        self.__input.capture()

    def exit(self):
        # キーボード情報取得
        key_data = self.__input.get_string()

        #ここにDBと照合する処理を入れる（暫定で直値を設定）
        key_return = True

        # 照合した結果：登録されている備品と一致した
        if key_return == True:
           self.__get_next_state = state.StandbyExpirationDateInputWhenUpdate()

        # 照合した結果：何らかの原因で登録されている備品と一致しなかった
        if key_return == False:
            Console.puts("機材ID「%s」を受理できませんでした。" % key_data)
            Console.puts("再度試しても失敗する場合、システム管理者に問い合わせてください。")
        #    Console.puts(">",end="")
            self.__get_next_state = state.ErrorHasOccurred()

    def get_next_state(self):
            return self.__get_next_state

    def should_exit(self):
            return self.__input.submitted()
