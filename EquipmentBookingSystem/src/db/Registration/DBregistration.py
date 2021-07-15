#!/usr/bin/env python

def DBregistration_EmpIDtoEmpNo(EmpID,EmpNo):
    # 社員証から読み取ったID(EmpID)が手打ちした社員番号に紐付くようユーザーを登録したDBに登録する
    # 登録できた場合「True」と返す
    # 登録できなかった場合「False」と返す

    # 仮の戻り値
    ret = True

    return ret

def DBregistration_Borrow(EquID,EmpNo,RetDay):
    # 備品を登録したDBの備品ステータスを借用中に登録する
    #   対象備品(RquID)と社員番号（EquNo）と返却予定日(RetDay)は必須
    #   借用開始日は自動取得
    # 登録できた場合「True」と返す
    # 登録できなかった場合「False」と返す
    
    # 仮の戻り値
    ret = True

    return ret

def DBregistration_Return(EquID):
    # 備品を登録したDBの備品ステータスを借用可能（返却済み）に登録する
    #   対象備品(RquID)は必須
    # 登録できた場合「True」と返す
    # 登録できなかった場合「False」と返す
    
    # 仮の戻り値
    ret = True

    return ret

def DBregistration_Update(EquID,RetDay):
    # 備品を登録したDBの対象備品の返却予定日のみを更新する
    #   対象備品(RquID)と返却予定日(RetDay)は必須
    # 登録できた場合「True」と返す
    # 登録できなかった場合「False」と返す
    
    # 仮の戻り値
    ret = True

    return ret

if __name__ == "__main__":
    ret = DBregistration_EmpIDtoEmpNo("114","514")
    print(ret)

    ret = DBregistration_Borrow("11","45","14")
    print(ret)

    ret = DBregistration_Return("114514")
    print(ret)
    
    ret = DBregistration_Update("114","514")
    print(ret)
