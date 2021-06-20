#!/usr/bin/env python


if __name__ == "__main__":
    import time
    import sys
    sys.path.append('../')
    sys.path.append('../../')

import dev.display as display
import dev.input as input


# Not implemented yet.
class RFIDReader(input.IUserInputReader):
    def __init__(self):
        pass

    def capture(self):
        pass

    def get_string(self):
        return ""

    def submitted(self):
        return False


def debug_this_module():
    pass


if __name__ == "__main__":
    help(debug_this_module)
    time.sleep(1)
    debug_this_module()
