#!/usr/bin/env python

import os
import pandas as pd
from datetime import datetime
import config

filepath_user = config.get_user_db_path()
filepath_item = config.get_equipment_db_path()


def DBregistration_EmpIDtoEmpNo(EmpID, EmpNo):
    # 社員証から読み取ったID(EmpID)が手打ちした社員番号に紐付くようユーザーを登録したDBに登録する
    # 登録できた場合「True」と返す
    # 登録できなかった場合「False」と返す

    # encodingはshift-jisがエラー出るのでcp932を使用
    df_csv = pd.read_csv(filepath_user, encoding="cp932")

    # 空白が欠損値NaNで取り込まれたままだと後工程でエラーとなるので「-」で埋める
    df_tmpcsv = df_csv.fillna("-")

    # 処理内容は同じはずだがうまく動かなかったので記載方法変更。
    #df_tgt = df_tmpcsv.query('ユーザID == {}'.format(EmpNo))
    df_tgt = df_tmpcsv.query('ユーザID == @EmpNo')

    # DB登録と戻り値設定
    if len(df_tgt) == 1:
        # 書き戻すデータは「-」埋めしてないデータにする。
        df_csv.iat[df_tgt.index.values[0],
                   df_tgt.columns.get_loc('備考')] = EmpID
        df_csv.to_csv(filepath_user, index=False,
                      header=True, encoding="cp932", mode='w')

        # バックアップを出力
        # タイムスタンプは「年月日_時分秒」で取得
        add_time = datetime.now().strftime('%Y%m%d_%H%M%S_')
        bkupfilepath = filepath_user.replace(os.path.basename(
            filepath_user), "BKUP_" + add_time + os.path.basename(filepath_user))
        df_csv.to_csv(bkupfilepath, index=False, header=True,
                      encoding="cp932", mode='w')

        ret = True
    elif len(df_tgt) > 1:
        # 不正登録（多重登録）はないはずなので仮実装※登録失敗で返す
        ret = False
    else:
        # DBに登録されてない場合は登録しない。
        ret = False

    return ret


def DBregistration_Borrow(EquID, EmpNo, RetDay):
    # 備品を登録したDBの備品ステータスを借用中に登録する
    #   対象備品(EquID)と社員番号（EmpNo）と返却予定日(RetDay)は必須
    #   借用開始日は自動取得
    # 登録できた場合「True」と返す
    # 登録できなかった場合「False」と返す

    # encodingはshift-jisがエラー出るのでcp932を使用
    df_csv = pd.read_csv(filepath_item, encoding="cp932")

    # 空白が欠損値NaNで取り込まれたままだと後工程でエラーとなるので「-」で埋める
    df_tmpcsv = df_csv.fillna("-")

    # 処理内容は同じはずだがうまく動かなかったので記載方法変更。
    df_tgt = df_tmpcsv.query('タグID == {}'.format(EquID))
    #df_tgt = df_tmpcsv.query('タグID == @EquID')

    # 借用開始日は本手続きをした日で固定
    brw_day = datetime.now().strftime('%Y/%m/%d')

    # DB登録と戻り値設定
    if len(df_tgt) == 1:
        # 借用可能なら貸し出し処理する
        if df_csv.iat[df_tgt.index.values[0], df_tgt.columns.get_loc('内容')] == "借用可能":
            # 書き戻すデータは「-」埋めしてないデータにする。
            df_csv.iat[df_tgt.index.values[0],
                       df_tgt.columns.get_loc('ユーザID')] = EmpNo
            df_csv.iat[df_tgt.index.values[0],
                       df_tgt.columns.get_loc('開始日付')] = brw_day
            df_csv.iat[df_tgt.index.values[0],
                       df_tgt.columns.get_loc('終了日付')] = RetDay
            df_csv.iat[df_tgt.index.values[0],
                       df_tgt.columns.get_loc('内容')] = "借用中"
            df_csv.to_csv(filepath_item, index=False,
                          header=True, encoding="cp932", mode='w')

            # バックアップを出力
            # タイムスタンプは「年月日_時分秒」で取得
            add_time = datetime.now().strftime('%Y%m%d_%H%M%S_')
            bkupfilepath = filepath_item.replace(os.path.basename(
                filepath_item), "BKUP_" + add_time + os.path.basename(filepath_item))
            df_csv.to_csv(bkupfilepath, index=False, header=True,
                          encoding="cp932", mode='w')

            ret = True
        else:
            ret = False

    elif len(df_tgt) > 1:
        # 不正登録（多重登録）はないはずなので仮実装※登録失敗で返す
        ret = False
    else:
        # DBに登録されてない場合は登録しない。
        ret = False

    return ret


def DBregistration_Return(EquID):
    # 備品を登録したDBの備品ステータスを借用可能（返却済み）に登録する
    #   対象備品(RquID)は必須
    # 登録できた場合「True」と返す
    # 登録できなかった場合「False」と返す

    # encodingはshift-jisがエラー出るのでcp932を使用
    df_csv = pd.read_csv(filepath_item, encoding="cp932")

    # 空白が欠損値NaNで取り込まれたままだと後工程でエラーとなるので「-」で埋める
    df_tmpcsv = df_csv.fillna("-")

    # 処理内容は同じはずだがうまく動かなかったので記載方法変更。
    df_tgt = df_tmpcsv.query('タグID == {}'.format(EquID))
    #df_tgt = df_tmpcsv.query('タグID == @EquID')

    # DB登録と戻り値設定
    if len(df_tgt) == 1:
        # 借用中なら返却処理する
        if df_csv.iat[df_tgt.index.values[0], df_tgt.columns.get_loc('内容')] == "借用中":
            # 書き戻すデータは「-」埋めしてないデータにする。
            df_csv.iat[df_tgt.index.values[0],
                       df_tgt.columns.get_loc('ユーザID')] = "-"
            df_csv.iat[df_tgt.index.values[0],
                       df_tgt.columns.get_loc('開始日付')] = "-"
            df_csv.iat[df_tgt.index.values[0],
                       df_tgt.columns.get_loc('終了日付')] = "-"
            df_csv.iat[df_tgt.index.values[0],
                       df_tgt.columns.get_loc('内容')] = "借用可能"
            df_csv.to_csv(filepath_item, index=False,
                          header=True, encoding="cp932", mode='w')

            # バックアップを出力
            # タイムスタンプは「年月日_時分秒」で取得
            add_time = datetime.now().strftime('%Y%m%d_%H%M%S_')
            bkupfilepath = filepath_item.replace(os.path.basename(
                filepath_item), "BKUP_" + add_time + os.path.basename(filepath_item))
            df_csv.to_csv(bkupfilepath, index=False, header=True,
                          encoding="cp932", mode='w')

            ret = True
        else:
            ret = False

    elif len(df_tgt) > 1:
        # 不正登録（多重登録）はないはずなので仮実装※登録失敗で返す
        ret = False
    else:
        # DBに登録されてない場合は登録しない。
        ret = False

    return ret


def DBregistration_Update(EquID, RetDay):
    # 備品を登録したDBの対象備品の返却予定日のみを更新する
    #   対象備品(RquID)と返却予定日(RetDay)は必須
    # 登録できた場合「True」と返す
    # 登録できなかった場合「False」と返す

    # encodingはshift-jisがエラー出るのでcp932を使用
    df_csv = pd.read_csv(filepath_item, encoding="cp932")

    # 空白が欠損値NaNで取り込まれたままだと後工程でエラーとなるので「-」で埋める
    df_tmpcsv = df_csv.fillna("-")

    # 処理内容は同じはずだがうまく動かなかったので記載方法変更。
    df_tgt = df_tmpcsv.query('タグID == {}'.format(EquID))
    #df_tgt = df_tmpcsv.query('タグID == @EquID')

    # DB登録と戻り値設定
    if len(df_tgt) == 1:
        # 借用中なら返却日更新処理する
        if df_csv.iat[df_tgt.index.values[0], df_tgt.columns.get_loc('内容')] == "借用中":
            # 書き戻すデータは「-」埋めしてないデータにする。
            df_csv.iat[df_tgt.index.values[0],
                       df_tgt.columns.get_loc('終了日付')] = RetDay
            df_csv.to_csv(filepath_item, index=False,
                          header=True, encoding="cp932", mode='w')

            # バックアップを出力
            # タイムスタンプは「年月日_時分秒」で取得
            add_time = datetime.now().strftime('%Y%m%d_%H%M%S_')
            bkupfilepath = filepath_item.replace(os.path.basename(
                filepath_item), "BKUP_" + add_time + os.path.basename(filepath_item))
            df_csv.to_csv(bkupfilepath, index=False, header=True,
                          encoding="cp932", mode='w')

            ret = True
        else:
            ret = False

    elif len(df_tgt) > 1:
        # 不正登録（多重登録）はないはずなので仮実装※登録失敗で返す
        ret = False
    else:
        # DBに登録されてない場合は登録しない。
        ret = False

    return ret


if __name__ == "__main__":
    #ret = DBregistration_EmpIDtoEmpNo("181818","79348")
    # print(ret)

    ret = DBregistration_Borrow("101", "79348", "2021/08/26")
    print(ret)
    ret = DBregistration_Borrow("102", "79348", "2021/08/26")
    print(ret)
    ret = DBregistration_Borrow("201", "79348", "2021/08/26")
    print(ret)

    ret = DBregistration_Return("102")
    print(ret)
    ret = DBregistration_Return("201")
    print(ret)
    ret = DBregistration_Return("202")
    print(ret)

    ret = DBregistration_Update("101", "2021/09/01")
    print(ret)
    ret = DBregistration_Update("102", "2021/09/01")
    print(ret)
    ret = DBregistration_Update("201", "2021/09/01")
    print(ret)
