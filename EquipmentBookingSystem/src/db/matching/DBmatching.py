#!/usr/bin/env python

import os
import pandas as pd
import config

filepath_user = config.get_user_db_path()
filepath_item = config.get_equipment_db_path()


def DBmatching_EmpIDtoEmpNo(EmpID):
    # 社員証から読み取ったID(EmpID)をユーザーを登録したDBと照合する
    # 登録済みユーザーなら社員番号を返す
    # 未登録ユーザーなら「False」と返す

    # encodingはshift-jisがエラー出るのでcp932を使用
    df_csv = pd.read_csv(filepath_user, encoding="cp932")

    # 空白が欠損値NaNで取り込まれたままだと後工程でエラーとなるので「-」で埋める
    df_csv = df_csv.fillna("-")

    df_Emp = df_csv.query('備考 == {}'.format(EmpID))

    # 戻り値設定
    if len(df_Emp) == 1:
        EmpNo = df_Emp.iat[0, df_Emp.columns.get_loc('ユーザID')]
    elif len(df_Emp) > 1:
        # 不正登録（多重登録）はないはずなので仮実装※未登録で返す
        EmpNo = False
    else:
        EmpNo = False

    return EmpNo


def DBmatching_EquIDtoEquStatus(EquID):
    # 備品タグから読み取ったIDを備品を登録したDBと照合する
    # 登録済み備品なら借用状況を返す
    #   0：未登録
    #   1：借用可能
    #   2：借用中
    #   3：故障中
    #   4：DBメンテミス

    # encodingはshift-jisがエラー出るのでcp932を使用
    df_csv = pd.read_csv(filepath_item, encoding="cp932")

    # 空白が欠損値NaNで取り込まれたままだと後工程でエラーとなるので「-」で埋める
    df_csv = df_csv.fillna("-")

    df_Equ = df_csv.query('タグID == {}'.format(EquID))

    # 戻り値設定
    if len(df_Equ) == 1:
        if df_Equ.iat[0, df_Equ.columns.get_loc('内容')] == "借用可能":
            EquStatus = 1
        elif df_Equ.iat[0, df_Equ.columns.get_loc('内容')] == "借用中":
            EquStatus = 2
        elif df_Equ.iat[0, df_Equ.columns.get_loc('内容')] == "故障中":
            EquStatus = 3
        else:
            # DBの「内容」欄のメンテミスを想定
            EquStatus = 4

    elif len(df_Equ) > 1:
        # 不正登録（多重登録）はないはずなので仮実装※未登録で返す
        EquStatus = 0
    else:
        EquStatus = 0

    return EquStatus


def DBmatching_EquIDtoEquName(EquID):
    # 備品タグから読み取ったIDを備品を登録したDBと照合する
    # 登録済み備品なら備品名を返す
    # 未登録備品なら「False」と返す

    # encodingはshift-jisがエラー出るのでcp932を使用
    df_csv = pd.read_csv(filepath_item, encoding="cp932")

    # 空白が欠損値NaNで取り込まれたままだと後工程でエラーとなるので「-」で埋める
    df_csv = df_csv.fillna("-")

    df_Equ = df_csv.query('タグID == {}'.format(EquID))

    # 戻り値設定
    if len(df_Equ) == 1:
        EquName = df_Equ.iat[0, df_Equ.columns.get_loc('施設ID')]
    elif len(df_Equ) > 1:
        # 不正登録（多重登録）はないはずなので仮実装※未登録で返す
        EquName = False
    else:
        EquName = False

    return EquName


if __name__ == "__main__":
    ret = DBmatching_EmpIDtoEmpNo("114514")
    print(ret)
    ret = DBmatching_EmpIDtoEmpNo("000000")
    print(ret)

    ret = DBmatching_EquIDtoEquStatus("101")
    print(ret)
    ret = DBmatching_EquIDtoEquStatus("102")
    print(ret)
    ret = DBmatching_EquIDtoEquStatus("201")
    print(ret)
    ret = DBmatching_EquIDtoEquStatus("302")
    print(ret)

    ret = DBmatching_EquIDtoEquName("101")
    print(ret)
    ret = DBmatching_EquIDtoEquName("102")
    print(ret)
    ret = DBmatching_EquIDtoEquName("201")
    print(ret)
    ret = DBmatching_EquIDtoEquName("302")
    print(ret)
