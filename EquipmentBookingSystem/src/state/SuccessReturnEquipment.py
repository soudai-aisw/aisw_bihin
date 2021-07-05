#!/usr/bin/env python

import state as state
import dev.display.Console as Console
import dev.input as input

# いるんかわからん(理解してない)
input.path.append('../../')

class SuccessReturnEquipment(state.IState):
    def entry(self):
        Console.puts("備品の返却が完了しました")
        Console.puts(">",end="")
