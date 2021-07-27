#!/usr/bin/env python



import state as state
import dev.display.Console as Console
import dev.input as input

class StandbyUserProcedureInput(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("手続き内容を選択してください","1:借用","2:返却","3:更新")
        Console.puts(">", end="")
        self.__input = input.UserInputReader()
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        procedure_type = self.__input.get_string()
        if( "1" == procedure_type ):
            self.__get_next_state = state.StandbyBarrowEquipmentIdRead()
        elif( "2" == procedure_type ):
            self.__get_next_state = state.StandbyReturnEquipmentIdRead()
        elif( "3" == procedure_type ):
            self.__get_next_state = state.StandbyUpdateEquipmentIdInput()
        else:
            Console.puts("不正なデータが入力されました。")
            Console.puts("再度入力してください。")
            Console.puts("")

        state.CommonResource.enquiry = procedure_type

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
