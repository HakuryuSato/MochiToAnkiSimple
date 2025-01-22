# Mochi to Anki Simple

A Python script for importing cards from Mochi to Anki.

## 前提
Mochi APIを使用するためproプランへサブスクが必要

## 使い方
1. MochiからAPIキー取得(サブスクが必要)し、.envにMOCHI_API_KEY="あなたのAPIKEY"の形式で記述
2. Ankiをインストールし、Anki Connectを追加、Ankiを起動しておく
3. main.pyを実行


## スクリプトの処理
1.Mochiから全デッキ取得
2.Mochiから全カード情報を取得し
3.取得したカード情報をjsonへ一時保存
4.Anki用にcsvに変換（問題,解答 の形式で、デッキ名.csvで保存）
5.ankiへデッキ名、問題、解答の情報を書き込む


## ファイル構成

