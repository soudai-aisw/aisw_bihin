#!/usr/bin/env python

def DBmatching_EmpIDtoEmpNo(EmpID):
    # 社員証から読み取ったID(EmpID)をユーザーを登録したDBと照合する
    # 登録済みユーザーなら社員番号を返す
    # 未登録ユーザーなら「False」と返す
    
    # 仮の戻り値
    EmpNo = "0079522"

    return EmpNo

def DBmatching_EquIDtoEquStatus(EquID):
    # 備品タグから読み取ったIDを備品を登録したDBと照合する
    # 登録済み備品なら借用状況を返す
    #   1：借用可能
    #   2：借用中
    #   3：故障中
    # 未登録備品なら「False」と返す
    
    # 仮の戻り値
    EquStatus = 1

    return EquStatus

if __name__ == "__main__":
    ret = DBmatching_EmpIDtoEmpNo("114514")
    print(ret)

    ret = DBmatching_EquIDtoEquStatus("114514")
    print(ret)

