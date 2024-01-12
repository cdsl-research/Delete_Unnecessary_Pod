# Delete_Unnecessary_Pod
Kubernetesの講義で使用することを想定しています．Kubernetesを用いて作成されたPodを削除します．
Googleスプレッドシートで課題の進捗を管理し，削除対象を決定します．
[delete_pod.py](https://github.com/cdsl-research/c0a21069/blob/f31273585a660dac255fac8f062734cdbce5884c/delete_pod.py)はUbuntu 22.04を搭載した仮想マシンで実行しました．

## 注意
Googleスプレッドシートの拡張機能であるApps Scriptを使用します．
Googleスプレッドシートを読み取るためにGoogle Sheets APIを使用します．
historyコマンドでコマンドの実行時刻を取得できるようにする必要があります．

## 使い方
[delete_pod.py](https://github.com/cdsl-research/c0a21069/blob/f31273585a660dac255fac8f062734cdbce5884c/delete_pod.py)を仮想マシンに配置します．
```
sudo python3 delete_pod.py
```
で実行します．各ユーザーの.bash_historyを参照するためroot権限で実行する必要があります．

## Googleスプレッドシート
下のような課題の進捗を管理するスプレッドシートを用意します．

![スクリーンショット 2023-12-06 123602](https://github.com/cdsl-research/c0a21069/assets/85731531/d9388837-f74f-406d-9993-9767e58636ce)

スプレッドシートの編集履歴を記録するスプレッドシートを用意します．初めは白紙で，スプレッドシートが編集されると下のように記録されます．

![スクリーンショット 2023-12-21 104555](https://github.com/cdsl-research/c0a21069/assets/85731531/7c4d28c4-baa2-4484-9709-7a1b75062a1d)


## [delete_pod.py](https://github.com/cdsl-research/c0a21069/blob/f31273585a660dac255fac8f062734cdbce5884c/delete_pod.py)
### グローバル変数
#### sheets_id
spreadsheetIdを入れる．
#### api_key
APIキーを入れる．
### 関数
#### get_user
Ubuntuのユーザーを取得し，スプレッドシートの学籍番号と一致するユーザーをリストで返します．
#### get_path
指定された拡張子のファイルの絶対パスを取得し，リストで返します．
#### get_history
get_userで取得したユーザーの.bash_historyからkubectl applyを取得し，実行時刻とコマンドをリストで返します．
#### get_progress
課題の進捗を管理するスプレッドシートを読み取り，JSONファイルとして保存します．

保存したJSONファイルから対応するグループの課題の進捗をリストで返します．
#### get_log
スプレッドシートの変更履歴を記録したスプレッドシートを読み取り，JSONファイルとして保存します．

保存したJSONファイルから対応する学生のスプレッドシートの編集履歴をリストで返します．
#### delete_command
get_log，kadai_progress，get_historyで取得したリストから実行するコマンドを決定します．
#### run_delete
delete_commandで取得したコマンドを実行します．

## [history.sh](https://github.com/cdsl-research/c0a21069/blob/705a5733536832b2f47a49f6ec212f473a4517e8/history.sh)
Ubuntuのhistoryコマンドでコマンドの実行時刻を取得できるようにします．/etc/profile.dに配置します．

## [log.gs](https://github.com/cdsl-research/c0a21069/blob/950cd285916e0302e25744507ccd0a9065f3b6e1/log.gs)
Googleスプレッドシートの拡張機能であるApps Scriptで使用します．
