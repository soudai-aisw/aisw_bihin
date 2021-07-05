#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input

# いるんかわからん(理解してない)
input.path.append('../../')

class StandbyReturnEquipmentRead(state.IState):
    def entry(self):
        Console.puts("返却する備品のRFIDをかざしてください")
        Console.puts(">",end="")

    def do(self):
        # RFID入力受付(適当)
        input.rfid_wait

    def exit(self):
        # rfid値初期化
        rfid_id = self.__input.get_string()

        # 勝手にDBから情報もってきて配列に入れる想定
        # 0: employeeID
        # 1: enquiry
        # 2: expirationDate
        # 3: prev_state
        # 4: 登録番号？
        # 5: 機材名
        rfid_return = []

        #ここにDBと照合する処理を入れる##################################
        #
        #
        ##############################################################

        # かざされたRFIDがDB照合結果、貸し出されているものだった場合(今は仮値)
        if rfid_return[0] == "0079591" and rfid_return[2] != 0:
            self.__get_next_state = state.SuccessReturnEquipment()

        # かざされたRFIDがDB上貸し出されていない場合(今は仮値)
        if rfid_return[2] == "":
            Console.puts("貸し出されていない備品です。")
            Console.puts(">",end="")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDがDB上登録されていない場合(今は仮値)
        if rfid_return[4] == "":
            Console.puts("登録されていない備品です。")
            Console.puts(">",end="")
            self.__get_next_state = state.ErrorHasOccurred()

    def get_next_state(self):
            return self.__get_next_state

    def should_exit(self):
            return self.__input.submitted()
