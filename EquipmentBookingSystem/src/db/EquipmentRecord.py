#!/usr/bin/env python

from db.Record import Record


class EquipmentRecord(Record):
    USER_ID = "ユーザID"
    EQUIPMENT_ID = "施設ID"
    RFID = "タグID"
    STATUS = "内容"
    BEGIN_DATE = "開始日付"
    END_DATE = "終了日付"

    def _dict_init(self):
        return {
            EquipmentRecord.EQUIPMENT_ID: "-",
            EquipmentRecord.USER_ID: "-",
            "利用目的": "-",
            EquipmentRecord.BEGIN_DATE: "0",
            "開始時刻": "0",
            EquipmentRecord.END_DATE: "0",
            "終了時刻": "0",
            EquipmentRecord.STATUS: "借用可能",
            "編集権限": "0",
            "公開区分": "0",
            "担当部署": "-",
            "担当・使用者名": "-",
            "人数": "-",
            "利用区分": "-",
            "連絡先": "-",
            "会議名案内": "-",
            "駐車場見込み台数": "-",
            "印刷区分": "-",
            "行き先": "-",
            EquipmentRecord.RFID: "0"
        }

    def _validate(self, key, value):
        return True
        