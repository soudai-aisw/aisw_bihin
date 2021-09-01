#!/usr/bin/env python

from db.Record import Record


class AccountRecord(Record):
    EMPLOYEE_ID = "ユーザID"
    FIRST_NAME = "名"
    LAST_NAME = "姓"
    RFID = "備考"

    def _dict_init(self):
        return {
            AccountRecord.EMPLOYEE_ID: "0",
            "ワンタイムパスワード通知先メールアドレス": "",
            "社員/職員番号": "",
            AccountRecord.LAST_NAME: "",
            AccountRecord.FIRST_NAME: "",
            "氏名(姓カナ)": "",
            "氏名(名カナ)": "",
            "ログイン停止": "0",
            "所属": "",
            "役職": "",
            "ソートキー1": "",
            "ソートキー2": "",
            "性別": "1",
            "入社年月日(西暦)": "",
            "生年月日(西暦)": "",
            "生年月日公開フラグ": "0",
            "メールアドレス１": "",
            "メールアドレスコメント１": "",
            "メールアドレス１公開フラグ": "0",
            "メールアドレス２": "",
            "メールアドレスコメント２": "",
            "メールアドレス２公開フラグ": "0",
            "メールアドレス３": "",
            "メールアドレスコメント３": "",
            "メールアドレス３公開フラグ": "0",
            "郵便番号": "",
            "郵便番号公開フラグ": "0",
            "都道府県コード": "0",
            "都道府県公開フラグ": "0",
            "住所１": "",
            "住所１公開フラグ": "0",
            "住所２": "",
            "住所２公開フラグ": "0",
            "電話番号１": "",
            "電話番号内線１": "",
            "電話番号コメント１": "",
            "電話番号１公開フラグ": "0",
            "電話番号２": "",
            "電話番号内線２": "",
            "電話番号コメント２": "",
            "電話番号２公開フラグ": "0",
            "電話番号３": "",
            "電話番号内線３": "",
            "電話番号コメント３": "",
            "電話番号３公開フラグ": "0",
            "ＦＡＸ１": "",
            "ＦＡＸコメント１": "",
            "ＦＡＸ１公開フラグ": "0",
            "ＦＡＸ２": "",
            "ＦＡＸコメント２": "",
            "ＦＡＸ２公開フラグ": "0",
            "ＦＡＸ３": "",
            "ＦＡＸコメント３": "",
            "ＦＡＸ３公開フラグ": "0",
            AccountRecord.RFID: ""
        }

    def _validate(self, key, value):
        return True
        