# neko-punch

## Use case

- admin がやること
  - wes server を deploy する fqdn を入力
  - cwl file を指定 (複数？)
- neko punch のやること
  - web component の src を生成
  - sapporo-service を register only mode で起動
  - CROS を設定
    - admin に fqdn を入力させるのが面倒だから、そもそも CROS いらんのでは？
    - register only mode かつ指定された workflow のみを許容しているため、別に困らないよね
      - job queue は設定しておく
  - cwltool --make-template

## Motivation

- うちのサーバーかしてあげるから、そこで決まった workflow を実行していいよ
  - blast の link が web genome browser についている的な
  - admin を楽させたい
    - 簡単であればあるほど良い
  - meta stanza とかも良い

## 設計メモ

- css 一個も当てないレベル
  - element に id 振っとく
- Web Form の POST ででかいファイルを送る問題
  - <https://jpostdb.org>
- web component の code は基本的に触らない
  - 人はいじらない
  - 簡単、ただしいじらせない
- user flow
  - user は parameter 入力
  - 実行 button を押す
  - WES Server に request が飛ぶ
  - WES Server から run_id が返ってくる
    - web storage に入れておく
  - wes server に更に、結果描写用の web app も併設しておいて、そこの url も返す？
    - or github pages に wes result viewer の web app を deploy しておく
