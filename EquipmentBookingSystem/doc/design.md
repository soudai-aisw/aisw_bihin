

<style>
h1,h2,h3,h4,h5 {
    font-weight: bold;
    border-bottom: inset 2px #000000;
}
</style>


# 1. Environment requirements

Undefined

# 2. Coding rule

PEP8を推奨します。
<https://pep8-ja.readthedocs.io/ja/latest/>

# 3. Design

本ソフトウェアの設計を示します。

## 3.1. Layer design

誰かいい感じに作って

```ditaa {cmd=true args=["-E"]}
  +----------------------------------+
  | User interface layer       cBLU  |
  +--+---------------------------+---+
     | Input                     ^
     v                   Display |
  +--+---------------------------+---+
  | Application layer          cGRE  |
  |                                  |
  +--+---------------------------+---+
     | Request                   ^ 
     v                  Responce | 
  +--+---------------------------+---+
  | Database controller        cYEL  |
  +--------------+-------------------+
                 |
            /----+-----\
            | {s}      |
            | Database |
            | (csv)    |
            \----------/
```

## 3.2. Directory

プロジェクトのディレクトリ構成を以下に示します。

```plantuml
scale 1.5
salt
{
    {T
        **Directory structure**                             | **Description**                       | **Layer**
         <&folder>src                                       | .
        + <&file>main.py                                    | アプリケーションのエントリポイント       | Application
        + <&file>StateController.py                         | アプリケーションの状態管理を行う         | Application
        + <&folder>cmn                                      | 共通モジュール                         | Library
        ++ <&file>~__init__.py                              | .
        ++ <&file>des_pattern.py                            | 共通デザインパターン
        + <&folder>dev                                      | デバイス                              | User interface
        ++ <&folder>display                                 | ディスプレイ
        +++ <&file>~__init__.py                             | .
        +++ <&file>Console.py                               | コンソールに対する操作を行うモジュール
        ++ <&folder>input                                   | .
        +++ <&file>~__init__.py                             | .
        +++ <&file>IUserInputReader.py                      | ユーザ入力標準インタフェースクラス
        +++ <&file>UserInputReader.py                       | ユーザ入力待ちを行うモジュール
        +++ <&file>consoleTextField.py                      | ユーザ入力(1行)を待機するモジュール
        +++ <&file>pressedKey.py                            | キー押下を監視するモジュール
        +++ <&file>singletonKeyboard.py                     | デバイスからキー入力を受け取るモジュール
        +++ <&file>RFIDReader.py                            | RFID
        + <&folder>state                                    | .                                     | Application
        ++ <&file>~__init__.py                              | .
        ++ <&file>commonResource.py                         | .
        ++ <&file>IState.py                                 | .
        ++ <&file>Init.py                                   | .
        ++ <&file>Restart.py                                | .
        ++ <&file>PreExit.py                                | .
        ++ <&file>Exit.py                                   | .
        ++ <&file>StandbyUserIdInput.py                     | .
        ++ <&file>ErrorHasOccurred.py                       | .
    }
}
caption **__Directory structure__**
```



## 3.3. Sequence from entry point

アプリケーションはmain.pyから開始します。main.py起動後のアプリケーションの簡易的なシーケンスを以下に示します。

```plantuml
scale 0.7
autoactivate on
hide footbox

participant "__<<static>>__\n__main__" as main
participant "__<<dynamic>>__\nclass StateController" as StateController
participant "__<<dynamic>>__\nclass pressedKey" as pressedKey
participant "__<<dynamic>>__\nclass singletonKeyboard\n**extend Thread**\n**extend Singleton**\n10msに一度実行" as singletonKeyboard
participant "__<<dynamic>>__\ninterface IState" as IState
participant "__<<static>>__\n__class commonResource__" as commonResource

activate main
main -> StateController ** : StateController():生成
activate StateController
    StateController -> IState ** : state.Init():生成
    activate IState
    return class instance
    StateController -> IState : __current.entry(): 状態開始
    deactivate

    StateController -> pressedKey **: pressedKey():生成
    activate pressedKey
        pressedKey -> singletonKeyboard **: singletonKeyboard():生成
        activate singletonKeyboard
        return class instance
        pressedKey -> singletonKeyboard : Thread.setDaemon(True):参照がなくなったら終了
        deactivate
        pressedKey -> singletonKeyboard : Thread.start()
        deactivate
    return class instance

return class instance
deactivate StateController

main -> StateController : run():実行
    loop __current != State.Exit() : 現在状態がExit以外の場合
        ... time.sleep(10) ...
        StateController -> pressedKey: capture()
            critical クリティカルセッション
            pressedKey -> singletonKeyboard: get_pressed_count()
            return
            pressedKey -> singletonKeyboard: get_last_pressed_key()
            return
            end
        deactivate

        StateController -> IState : __current.do():状態実行
        deactivate

        StateController -> IState : __current.should_exit()
        return 状態終了要否

        alt 状態終了すべき
            StateController -> IState : __current.exit():状態終了
            deactivate

            StateController -> IState : _current.get_next_state():次状態取得
            return 次状態

            StateController -> commonResource : prev_state = __current:現在状態を記憶
            deactivate

            StateController -> StateController : __current = 次状態:状態遷移
            deactivate

            StateController -> IState : __current.do():状態実行
            deactivate
        else 現在状態次のどちらでもない: State.Init(), State.Restart()
            opt エスケープキーが押された、又はタイムアウトを検知した
                StateController -> commonResource : prev_state = __current:現在状態を記憶
                deactivate
                StateController -> StateController : __current = state.Restart():Restartに遷移
                deactivate
                StateController -> IState : __current.do():状態実行
                deactivate
            end
        end
    end
    destroy singletonKeyboard
deactivate
caption **__Sequence diagram__**
```

## 3.4. dev.input package

キーボードやRFIDリーダーなどのデバイスから、ユーザ入力を受け取るパッケージです。特定のデバイスからの入力を要求しない場合、UserInputReaderを使用してください。

## 3.5. Class diagram

```plantuml
scale 0.8

package dev.input{
    interface IUserInputReader{
        ユーザ入力インタフェース
        ----
        + __init__(self):\n\t初期化を行います
        + capture(self):\n\t入力を監視します
        + get_string(self):\n\t入力された文字列を返します
        + submitted(self):\n\t入力が確定していればTrueを返します
    }

    class singletonKeyboard{
        キーボード入力を監視します。
        Thread.startで起動し、get_*インタフェースを使用する際は
        get_lock_objectでロックを獲得してください。
        入力ストリームは多重化できないためSingletonを実装しています。
        msvcrtを利用しているためLinux環境移植時は修正が必要です。
        ----
        + __init__(self):\n\t初期化を行います
        + run(self):\n\tスレッドを実行します
        + is_finished(self):\n\tスレッドが終了していればTrueを返します
        + get_last_pressed_key(self):\n\t最後に押されたキーを返します
        + get_pressed_count(self):\n\tキーが押された回数を返します
        + terminate(self):\n\tスレッドを終了します
        + get_lock_object(self):\n\tロックオブジェクトを取得します
    }

    class pressedKey{
        押されたキーを監視します。本クラスは複数生成可能です。
        ----
        + __init__(self):\n\t初期化を行います
        + capture(self):\n\tsingletonKeyboardを監視します
        + get(self):\n\t直前に押下されたキーを取得します
        + exists(self):\n\tキーが押されていればTrueを返します
        + is_escape(self):\n\tEscapeキーが押されていればTrueを返します
        + is_enter(self):\n\tEnterキーが押されていればTrueを返します
        + is_delete(self):\n\tDeleteキーが押されていればTrueを返します
    }

    class ConsoleTextField{
        テキストフィールドを提供します。
        ユーザがエンターキーを押下するまでに入力された
        文字列を返す機能を有します。
        ---
        + display_in_real_time(self, enabled):\n\tリアルタイム表示の要否を切り替えます
    }

    class RFIDReader{
        RFIDを読み取ります
    }

    class UserInputReader{
        RFID又はテキストフィールドからの
        入力を受け取ります。
    }
}
abstract Threading.Thread{
    スレッド機能を提供します。
}

class cmn.Singleton{
    本クラスを継承したクラスはシングルトンになり、
    クラス生成が1つしかできなくなります。
}

class msvcrt <<M,f6f>>{
    Microsoftが提供するWindows用の
    標準Cライブラリ機能を含むモジュールです。
}


singletonKeyboard -do-|> Threading.Thread : <<generalize>>
singletonKeyboard -do-|> cmn.Singleton : <<realize>>
singletonKeyboard -do-> msvcrt : <<delegate>>

pressedKey "*" -le--> "1" singletonKeyboard : <<delegate>>
ConsoleTextField -do-> pressedKey : <<delegate>>

ConsoleTextField -up-|> IUserInputReader : <<realize>>
RFIDReader -up-|> IUserInputReader : <<realize>>
UserInputReader -up-|> IUserInputReader : <<realize>>

UserInputReader -ri-> ConsoleTextField : <<delegate>>
UserInputReader -le-> RFIDReader : <<delegate>>

caption **__class diagram of dev.input__**
```

## 3.6. dev.display package

画面出力を司るパッケージです。Consoleモジュールからのみ構成されます。

```plantuml

package dev.display{
    class Console{
        画面出力を行います。Linux / Windowsに対応しています。
        ---
        + clear():\n\t画面をクリアします
        + puts(*objects, sep=' ', end='\\n', file=sys.stdout, flush=False):\n\tprintのラッパです。画面出力を行います。
        + remove_line():\n\tコンソール画面から1行消去します。
        + remove_char():\n\tコンソール画面から1文字消去します。
    }
}

caption **__class diagram of dev.display__**
```

## 3.7. status package

アプリケーションの状態を司るパッケージ群です。

## 3.8. class diagram

StateControllerはIStateを実装するクラスに対し、entry, do, exit等のメソッドを用いて状態遷移を実現します。StatePatternを用いています。

```plantuml


class StateController{
    各状態の実行と状態遷移を司ります。
}

package status{
    interface IState{
        状態インタフェースです。
        StateControllerに実行させる状態は、本インタフェースを実装してください。
        ---
        + entry(self):\n\t状態入場時の処理を記述します
        + do(self):\n\t状態実行時の処理を記述します
        + exit(self):\n\t状態終了時の処理を記述します
        + get_next_state(self):\n\t次状態を返します
        + should_exit(self):\n\texitすべきであればTrueを返してください
    }

    class commonResource{
        各状態から参照する共有リソースです。
        すべてのメンバはstaticです。
        ---
        + {static}employeeId:\n\t社員番号
        + {static}enquiry:\n\t問い合わせ番号
        + {static}expirationDate:\n\t返却期限
        + {static}prev_state:\n\t前回の状態
        + {static}initialize():\n\t全フィールドの初期化
    }

    class ConcreteState{
        IStateを実装する状態群です。
        具体的には以下のような状態が存在します。
        ..
        class Init
        class PreExit
        class Exit
        class Restart
        class ErrorHasOccurred
        class StandbyUserIdInput
        ...etc
        ※State machineを参照してください。
    }
}

StateController o-do->  IState
ConcreteState   -up-|> IState : <<realize>>
ConcreteState   -up->  commonResource : <<use>>
caption **__class diagram of state__**

```

## 3.9. state machine

ConcreteState間の遷移を以下に示します。

```plantuml
scale 0.7

state StateController{
    state entrySys <<entryPoint>>
    state exitSys <<exitPoint>>

    state "Procedure status" as proc {
        state entryProc <<entryPoint>>
        state exitProc <<exitPoint>>
        state entryToPrevState <<entryPoint>>
        state exitByError <<exitPoint>>

        state StandbyUserIdInput : 社員証をかざしてください
        state StandbyUserProcedureInput : 手続き内容を選択してください

        state StandbyReturnEquipmentIdRead : 返却する備品のRFIDをかざしてください
        state SuccessReturnEquipment : 機材XXXの返却を受付ました

        state StandbyBarrowEquipmentIdRead : 借用する備品のRFIDをかざしてください
        state StandbyExpirationDateInputWhenBarrow : 返却予定日を入力してください
        state SuccessBarrowEquipment : 受け付けました

        state StandbyUpdateEquipmentIdInput : 返却予定日を更新する機材をかざしてください
        state StandbyExpirationDateInputWhenUpdate : 返却予定日を入力してください
        state SuccessUpdateEquipment : 受け付けました

    }

    state Init : ようこそ備品管理システムへ
    state PreExit : もう1度ESCキーが入力されると終了します
    state Exit : アプリケーションを終了します
    state Restart : 終了要求を受付又はタイムアウトしました
    state ErrorHasOccured
}

[*] -do-> entrySys
entrySys -do-> Init

ErrorHasOccured -ri-> entryToPrevState 
exitByError -le-> ErrorHasOccured

Init -> PreExit : escape key was pressed
PreExit -do-> Exit : escape key was pressed
PreExit -le-> Init : 30 seconds elasped
Exit -up> exitSys
exitSys -ri-> [*]

Restart -ri-> Init : 5 seconds elapsed or any key was pressed

Exit -do[hidden]-> ErrorHasOccured

Init -do-> entryProc : Any key except the escape key was pressed
exitProc -up-> Restart : 30 seconds elapsed or escape key was pressed

entryProc -do-> StandbyUserIdInput
StandbyUserIdInput -do-> StandbyUserProcedureInput

StandbyUserProcedureInput -do-> StandbyReturnEquipmentIdRead
StandbyReturnEquipmentIdRead -do--> SuccessReturnEquipment
SuccessReturnEquipment -up-> StandbyReturnEquipmentIdRead

StandbyUserProcedureInput -do-> StandbyBarrowEquipmentIdRead
StandbyBarrowEquipmentIdRead -do-> StandbyExpirationDateInputWhenBarrow
StandbyExpirationDateInputWhenBarrow -do-> SuccessBarrowEquipment
SuccessBarrowEquipment -up-> StandbyBarrowEquipmentIdRead

StandbyUserProcedureInput -do-> StandbyUpdateEquipmentIdInput
StandbyUpdateEquipmentIdInput -do-> StandbyExpirationDateInputWhenUpdate
StandbyExpirationDateInputWhenUpdate -do-> SuccessUpdateEquipment
SuccessUpdateEquipment -up-> StandbyUpdateEquipmentIdInput

caption **__State machine of Console window__**

```
