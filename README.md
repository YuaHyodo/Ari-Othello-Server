# Ari-Othello-Server
online_othello_protocol対応の簡易的なオセロサーバー
# 概要
- Ari-Shogi-Server( https://github.com/YuaHyodo/Ari-Shogi-Server )のオセロ版(未完成)
- online_othello_protocol(仮)対応
- online_othello_protocolについてはここを参照のこと: https://github.com/YuaHyodo/online_othello_protocol
- ファイル・クラス・関数・変数名、出力されるメッセージ、実装方法、設計思想などに関する意見は受け付けておりません。 (不満があるなら自分で作ってください)

# すでにある機能・想定している使い方
## すでにある機能
- online_othello_protocolを使ったオセロの対局を行う機能
- 複数のプレーヤがログインした際にランダムにマッチングする機能
- ログをとる機能
- プレーヤの情報を保存・管理する機能
- 簡易的なレートをつける機能
- プレーヤーの情報を自動で読み取ってHTMLファイルに書き出す機能(以下、サンプル)
![スクリーンショット 2022-08-03 230135](https://user-images.githubusercontent.com/66828980/183107034-3a6c1943-f14c-4f9a-96cd-cc16783ee35a.png)

## 想定している使い方
- なし

# ちゃんと実装できてないところ・不具合
- 手番を持った対局者が行動しないと永久に対局が終わらない
- ログアウト関連の部分
- その他多数
