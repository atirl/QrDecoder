# QrDecoder
QRコードから文字列（テキストファイル）を出力するツール

## 概要
QRコード付き画像ファイルをドラッグすると、テキストファイルを出力する、コンソールアプリです

## 作成経緯
- web上でQRコードをテキスト化するようなツールは多いですが、万が一のセキュリティのためにローカル用が欲しかった  
- 別ツール「TotpHyoujer」用に、QRコードをテキスト化して鍵を抜き出すため

## 使い方
__GUIで動かしたい方:__  
「Releases」からQrDecoderの最新版zipファイルをダウンロードし解凍する。  
QRコード付きの画像ファイルをQrDecoder.exeにドラッグ＆ドロップしてください。

__python実行環境がある方、コマンドラインで動す方:__  
「Code」からQrDecoder.pyをダウンロード(exeでもいいですが…)  
そしてコマンドラインで  
```powershell
python QrDecoder.py sample.png
```
実行できない場合は以下のコマンドでライブラリをインストールしてください  
```powershell
python -m pip install zxing-cpp pillow
```

## ファイル構成
- QrDecoder.py：本体（これだけで動きます）  
- sample.png：pngサンプル  
- vbs.jpg：jpgサンプル  
- bat.gif：gifサンプル

## 開発環境
- windows11
- python3.15  
OS非依存の部分が多いと思いますが、Linuxでは試していません。inputとイメージファイルオープンなど、引っかかるかも。  