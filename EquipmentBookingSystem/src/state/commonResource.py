#!/usr/bin/env python

import state


class Enquiry():
    Invalid = ""
    Borrow = "1"
    Return = "2"
    Update = "3"


class CommonResource():
    employeeId = ""                 # 社員番号
    enquiry = Enquiry.Invalid       # 問い合わせ内容
    equipmentId = ""                # 機材ID
    expirationDate = ""             # 返却予定日
    prev_state = state.Init()

    @staticmethod
    def initialize():
        CommonResource.employeeId = ""                  # 社員番号
        CommonResource.enquiry = Enquiry.Invalid        # 問い合わせ内容
        CommonResource.equipmentId = ""                 # 機材ID
        CommonResource.expirationDate = ""              # 返却予定日
