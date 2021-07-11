#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input

class StandbyBarrowEquipmentIdRead(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("借用する備品のRFIDをかざしてください")
        Console.puts(">", end="")
        self.__input = input.UserInputReader()
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

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

        # かざされたRFIDがDB照合結果、貸し出されているものでなく登録されているものだった場合(今は仮値)
        if rfid_return[2] == "" and rfid_return[4] != "":
            self.__get_next_state = state.StandabyExpirationDateInputWhenBarrow

        # かざされたRFIDがDB上貸し出されている場合(今は仮値)
        if rfid_return[2] == "":
            Console.puts("貸し出されている備品です。")
            Console.puts(">",end="")
            self.__get_next_state = state.ErrorHasOccurred()

        # かざされたRFIDがDB上登録されていない場合(今は仮値)
        if rfid_return[4] == "":
            Console.puts("登録されていない備品です。")
            Console.puts(">",end="")
            self.__get_next_state = state.ErrorHasOccurred()

    def get_next_state(self):
        return state.StandabyExpirationDateInputWhenBarrow

    def should_exit(self):
        return self.__input.submitted()
