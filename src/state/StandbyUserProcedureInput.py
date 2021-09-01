#!/usr/bin/env python


import state as state
import dev.display.Console as Console
import dev.input as input
from .commonResource import Enquiry

class StandbyUserProcedureInput(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("手続き内容を選択してください", "{}:借用 {}:返却 {}:更新".format(
            Enquiry.Borrow, Enquiry.Return, Enquiry.Update))
        Console.puts(">", end="")
        self.__input = input.SunitizedString(
            input.ConsoleTextField()
        )
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        procedure_type = self.__input.get_string()
        if(Enquiry.Borrow == procedure_type):
            self.__get_next_state = state.StandbyBarrowEquipmentIdRead()
        elif(Enquiry.Return == procedure_type):
            self.__get_next_state = state.StandbyReturnEquipmentIdRead()
        elif(Enquiry.Update == procedure_type):
            self.__get_next_state = state.StandbyUpdateEquipmentIdInput()
        else:
            Console.puts("不正なデータが入力されました。")
            Console.puts("再度入力してください。")
            Console.puts("")

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
