#!/usr/bin/env python

if __name__ == "__main__":
    import time
    import sys
    sys.path.append('../')
    sys.path.append('../../')

import platform

if (platform.system() == 'Windows'):
    import dev.input as input

    class RFIDReader(input.IUserInputReader):
        def __init__(self):
            pass

        def capture(self):
            pass

        def get_string(self):
            return ""

        def submitted(self):
            return False

else:
    import RPi.GPIO as GPIO
    import dev.input.MFRC522 as MFRC522
    import signal

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # Not implemented yet.
    class RFIDReader():

        #
        def __init__(self):
            self.__continue_reading = True
            self.__submitted = False
            self.__ret_uid = ""
            GPIO.setwarnings(False)
            GPIO.cleanup()

        #
        def capture(self):

            self.__submitted = False
            if self.__continue_reading:

                (status, TagType) = MIFAREReader.MFRC522_Request(
                    MIFAREReader.PICC_REQIDL)
                (status, uid) = MIFAREReader.MFRC522_Anticoll()

                if status == MIFAREReader.MI_OK:
                    self.__ret_uid = str(
                        uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                    self.__continue_reading = False
                    self.__submitted = True

        #
        def get_string(self):
            return self.__ret_uid

        #
        def submitted(self):
            return self.__submitted

    #
    def debug_this_module():
        idr = RFIDReader()
        idr.__init__()
        ret_subm = idr.submitted()
        print(ret_subm)

        idr.capture()
        ret_subm = idr.submitted()
        print(ret_subm)

        ret_dat = idr.get_string()
        print(ret_dat)

    if __name__ == "__main__":
        help(debug_this_module)
        time.sleep(1)
        debug_this_module()
