#!/usr/bin/env python



import state as state
import dev.display.Console as Console
import dev.input as input

class StandbyUserIdInput(state.IState):
    def entry(self):
        Console.clear()
        Console.puts("社員証をかざしてください")
        Console.puts(">", end="")
        self.__input = input.UserInputReader()
        self.__get_next_state = state.ErrorHasOccurred()

    def do(self):
        self.__input.capture()

    def exit(self):
        employee_id = self.__input.get_string()
        if (employee_id != ""):
            Console.puts("社員番号「", employee_id, "」を問い合わせます")

            if (employee_id == "0079522"):
                state.CommonResource.employeeId = employee_id
            else:
                Console.puts("存在しない社員番号です")

            # 現状は未実装なので必ず失敗
            self.__get_next_state = state.StandbyUserProcedureInput()
#            self.__get_next_state = state.StandbyUserIdInput()
        else:
            self.__get_next_state = state.StandbyUserIdInput()

    def get_next_state(self):
        return self.__get_next_state

    def should_exit(self):
        return self.__input.submitted()
