# standbyreturnequipmenttdread

```plantuml

[*] --> StandbyUseProcedureInput
StandbyUseProcedureInput --> StandbyReturnEquipmentIdRead
StandbyUseProcedureInput : 返却を選択

state StandbyReturnEquipmentIdRead{

    state entry1
    entry1: 「返却する備品のRFIDをかざしてください」と表示
    state do1
    do1 : RFIDかざされるまで待機(30秒)
    do1 : Escボタン待機
    state if<<choice>>
    do1 -down-> if
    if --> Exit1 : 返却する備品のRFIDがかざされた
    if --> Exit2 : かざされたRFIDがDB上貸し出されていない場合
    if --> Exit3 : かざされたRFIDがDB上登録されていない
    if --> Exit4 : 30秒無操作
    if --> Exit5 : Esc操作受付

}

Exit1 --> SuccessReturnEquipment
Exit2 --> ErrorWasOccured
Exit3 --> ErrorWasOccured
Exit4 --> Restart
Exit5 --> Restart

state SuccessReturnEquipment{

    state entry2
    entry2: 「機材XXXの返却手続きが完了しました」と表示(30秒)
    state do2
    do2: none
    state exit2
    exit2: Restartに遷移

}

SuccessReturnEquipment --> Restart

```