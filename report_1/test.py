import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('prismatic-petal-198815-3422944891c6.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

print(gc)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1BRN450vJugBghpBPdqPvESoh0DRNXXqqvx1wIhDyQUQ'

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

#A1セルの値を受け取る
import_value = 0# int(worksheet.acell('A1').value)

#A1セルの値に100加算した値をB1セルに表示させる
export_value = import_value+100
worksheet.update_cell(1,2, export_value)
