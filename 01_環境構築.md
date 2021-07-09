# rasberry piの環境構築
---

<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=true} -->

<!-- code_chunk_output -->

- [# rasberry piの環境構築](#-rasberry-piの環境構築)
- [日本語入力](#日本語入力)
- [VSCODEのインストール](#vscodeのインストール)
- [git連携](#git連携)
- [リモート設定](#リモート設定)
- [デフォPythonバージョン変更](#デフォPythonバージョン変更)
- [RFIDリーダの接続](#RFIDリーダの接続)
- [RFIDリーダの使用準備](#RFIDリーダの使用準備)

<!-- /code_chunk_output -->

---

## rasberry piの環境構築
- (基本ポチポチいじって遊んでればできますが)mainブランチにあるpdfを参照してください(尾崎さんリンクありがとうございます)

## 日本語入力
- rasberry piではデフォルト(初期設定したらだけども)で日本語の**表示**はできるが、**入力はできない**。

  - [参考サイト](https://www.indoorcorgielec.com/resources/raspberry-pi/raspberry-pi-input-japanese/)

1. rasberryマーク→アクセサリ→LXターミナルを開く
1. 下記コマンドを入力し、続行
   ```code 
   sudo apt update
   sudo apt install ibus-mozc
1. インストール完了後、rasberryマーク→Shutdown→Reboot
1. 2パターンある。
    1. 画面右上に「A」が表示されている→設定完了。
    1. 画面右上に「JA」or「EN」が表示されている→アイコンクリック→日本語→Mozcに切り替える

---
## gitのインストール

- 下記を参照。
-[参考サイト](https://qiita.com/natacom/items/63cca20e24e3e864e485)

---

## VSCODEのインストール

- rasberry pi(というかLinux)でも問題なく使える。
    - [参考サイト](https://pimylifeup.com/raspberry-pi-visual-studio-code/)

1. [VSCODEのサイト](https://code.visualstudio.com/#alt-downloads)に行く。
1. ペンギンマークの下の「.deb」「ARM」を押す。
1. ダウンロードした.debファイルをダブルクリック(多分→に入ってる。/home/pi/Downloads)
1. 「Do you want to install this file?」→ install
1. indentity:pi password:ラズパイ本体へのログインパスワードを入力し、OKを押下
1. Installing packagesと表示され、進捗バーが完了するまで暇をつぶす。
1. インストール完了したら、rasberryマーク→アクセサリにVSCODEがあるはず。

---

## git連携

- gitクライアント(tortoiseとか)を入れなくてもVSCODEでできちゃうので推奨。
    - 前提条件
        - gitリポジトリ提供してるサービスのアカウントがある(bitbucketからクローンならbitbucketのアカウント,githubからクローンならgithubのアカウント)

- 下記ではgithubからリポジトリクローンする場合を説明する。
1. VSCODE左のアイコン群の真ん中らへんのgitマーク?ブランチマークをクリック
1. 「リポジトリをクローン」みたいなとこをクリック
1. 検索窓に「githubからクローン」ってのが出てくるのでクリック。
1. ブラウザが立ち上がって、連携する？みたいなこと聞かれるのでokする。
1. VSCODEに戻り、クローンしたいリポジトリ名をうつ。
1. どこにクローンするか聞かれるので、指定する(pi/home/workspace とかで良いと思う)

---

## リモート設定
-  [参考サイト](https://scratchpad.jp/raspberry-pi-3-model-b-plus-4/#toc1)

- xrdpのインストール
1. メニューを開く
1. 「設定」>「Add/Remove Software」を選択
1. 左上の検索窓に「xrdp」を入力し検索
1. 「Remote Desktop Protocol (RDP) server」が右側の検索結果に表示される
1. 「Remote Desktop Protocol (RDP) server」にチェックボックスを入れる
1. 右下のOKを押す
1. インストールが実行される

- リモートデスクトップ接続の確認
　接続元のWindowsPCからリモートデスクトップ接続でラズパイに接続する
  （ラズパイ側のIP確認は「ifconfig」コマンドもしくは「ip addr」コマンドにて確認）


---

## デフォPythonバージョン変更
-  [参考サイト](https://www.ingenious.jp/articles/howto/raspberry-pi-howto/python-3-change/)
    - たいていの場合、ラズパイ(ラズビアン)にはPython2系と3系が標準搭載されておりPython2系がデフォルトになっている。今後の簡便化のためにPython3系をデフォルトにする。

- Python3への変更
1. 「cd /usr/bin」コマンドを実行
1. 「sudo unlink python」コマンドを実行し、現在のPythonシンボリック削除
1. 「sudo ln -s python3 python」コマンドを実行し、Python3系へのシンボリックリンクを作成
1. 「python --version」コマンドを実行し、Python3系にバージョンが変更されているか確認


---

## RFIDリーダの接続
- 下記表のとおり、ラズパイ端子とRFIDリーダの端子を接続する

| ラズパイ側 Pin番号 | RFID側端子名 |
|:-----------|------------:|
| Pin 24       | SDA        |
| Pin 23       | SCK        |
| Pin 19     | MISO      | 
| (接続無し)       | IRQ        |
|  GND(Pin 6, 9, 14, 20, 25, 30, 34, 39のいずれか)        | GND          |
| Pin22       | RST       |
|  3.3V PWR(Pin 1, 17のいずれか)   | 3.3V     |


---

## RFIDリーダの使用準備
-  [参考サイト](https://qiita.com/nanbuwks/items/c502ba880fbb93f522b3)

- SPIの有効化
1. 「sudo raspi-config 」コマンドを実行し、コンフィグを開く
1. コンフィグ内の「5 Interfacing Options  Configure connections to peripherals」を選択
1. 表示内の「P4 SPI Enable/Disable automatic loading of SPI kernel module」を選択
1. 「Would you like the SPI interface to be enabled?」の選択に対して、「Yes」を選択
1.  raspi-configを終了して再起動


- SPI-py ライブラリインストール
1. 「git clone https://github.com/lthiery/SPI-Py.git」コマンドを実行し、GitからSPi-Pyライブラリファイルを持ってくる
1. 「cd SPI-Py」コマンドを実行し、落としてきたフォルダ内をカレントディレクトリにする
1. 「sudo python setup.py install」コマンドを実行し、SPI-Pyライブラリをインストールする

