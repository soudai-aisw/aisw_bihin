#!/usr/bin/env python

import dev.input as input
import platform

if __name__ == "__main__":
    import time
    import sys
    sys.path.append('../')
    sys.path.append('../../')

if (platform.system() == 'Windows'):
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
    ##import dev.display as display
    ##import dev.input as input

    import RPi.GPIO as GPIO
    import MFRC522
    import signal

    # Create an object of the class MFRC522
    # MIFAREReader = MFRC522.MFRC522()

    # Not implemented yet.
    class RFIDReader():
    ##class RFIDReader(input.IUserInputReader):
        
        def __init__(self):
            continue_reading = True
            pass
        
        #
        def capture(self):
            
            #(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            #(status,uid) = MIFAREReader.MFRC522_Anticoll()
            
            pass
        
        def get_string(self):
            
            MIFAREReader = MFRC522.MFRC522()
            continue_reading = True
            while continue_reading:
            
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                (status,uid) = MIFAREReader.MFRC522_Anticoll()

                if status == MIFAREReader.MI_OK:

                    ret_uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                    continue_reading = False
            GPIO.cleanup()
            return ret_uid 

        def submitted(self):
            return False

    def debug_this_module():
        pass

    if __name__ == "__main__":
        help(debug_this_module)
        time.sleep(1)
        debug_this_module()
        ret_dat = RFIDReader.get_string("")
        print(ret_dat)
