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
            Console.puts("借用ですね")
 #           self.__get_next_state = state.StandbyUserIdInput()
        elif( "2" == procedure_type ):
            Console.puts("返却ですね")
        elif( "3" == procedure_type ):
            Console.puts("更新ですね")
        else:
            Console.puts("無効な入力ですね")

        state.CommonResource.enquiry = procedure_type

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
