if __name__ == "__main__":
    import os
    import sys
#   sys.path.append('../')
#    sys.path.append('../../')
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dev.display.Console as Console

class UsePlace():
    Invalid = ""
    InAISW = "1"
    OutAISW = "2"
    Outsourcer = "3"

    def Check(inputplace):
        if inputplace == UsePlace.InAISW:
            return True
        elif inputplace == UsePlace.OutAISW:
            return True
        elif inputplace == UsePlace.Outsourcer:
            return True
        else:
            Console.puts(inputplace + "は無効な場所です。")
            return False

    def ReturnName(inputplace):
        if inputplace == UsePlace.InAISW:
            return "1:社内"
        elif inputplace == UsePlace.OutAISW:
            return "2:社外"
        elif inputplace == UsePlace.Outsourcer:
            return "3:委託"
        else:
            Console.puts(inputplace + "は無効な場所です。")
            return ""


# -----------------------------------------------------------------------------

def __debug_this_module():
    str = input('Input Use Place:')
    result = UsePlace.Check(str)
    print(result)
    result = UsePlace.ReturnName(str)
    print(result)

if __name__ == "__main__":
    __debug_this_module()