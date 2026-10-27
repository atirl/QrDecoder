#============================================================
# QrDecoder : QRコードテキスト化ツール
# 2023/06/11 atirl　作成
# 2026/10/21 日本語ファイル対応、exe化対応
# 2026/10/25 exe化時、zxingcppのほうが遥かに軽いようなので変更
# 2026/10/27 TOTPのQRコードの場合、秘密鍵のみを出力できるように変更
#============================================================
import sys
import traceback
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from PIL import Image
import zxingcpp

#ファイル名用タイムスタンプ
def create_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

#エラーログ出力
def write_error(folder, message):
    filename = folder / f"qrFailed_{create_timestamp()}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(message)

    print(message)
    print(f"\nエラーログ出力: {filename}")

#TOTP判断と鍵の抜き出し
def extract_totp_secret(data):
    try:
        parsed = urlparse(data)

        # otpauth://totp/ 形式のURIだけを対象にする
        if parsed.scheme.lower() != "otpauth":
            return None

        if parsed.netloc.lower() != "totp":
            return None

        # クエリパラメーターを解析する
        params = parse_qs(parsed.query)

        #secretが存在しない場合は対象外
        secrets = params.get("secret")

        if not secrets or not secrets[0]:
            return None

        secret = secrets[0]

        #issuerは任意項目
        issuers = params.get("issuer")
        issuer = issuers[0] if issuers and issuers[0] else ""

        return secret, issuer

    except (ValueError, UnicodeError):
        #URI解析に失敗したら通常のテキストとして扱う
        return None


def main():

    if len(sys.argv) < 2:
        raise Exception("QRコード画像をドラッグしてください。")

    image_file = sys.argv[1]
    image_path = Path(image_file)

    #QRコードを読み取る
    try:
        with Image.open(image_path) as img:
            barcode = zxingcpp.read_barcode(
                img,
                formats=zxingcpp.BarcodeFormat.QRCode
            )
    except Exception as e:
        raise Exception(
            f"画像を開けません……\n\nファイル:\n{image_file}"
        ) from e

    if barcode is None:
        raise Exception("QRコードが検出できませんでした。画像を確認してください。")

    data = barcode.text

    #TOTP抜き出し関数呼び出し
    totp_data = extract_totp_secret(data)

    if totp_data is not None:
        secret, issuer = totp_data

        answer = input(
            "TOTP秘密鍵を検出しました。"
            "秘密鍵のみを出力しますか? (yes/no): "
        ).strip().lower()

        if answer == "yes":

            #ファイル名に使えない文字を置き換える
            safe_issuer = "".join(
                "_" if c in '<>:"/\\|?*' else c
                for c in issuer
            ).strip(" .")

            #issuerがない場合はnoIssuerとする
            if not safe_issuer:
                safe_issuer = "noIssuer"

            output_file = (
                image_path.parent /
                f"qrKey_{safe_issuer}_{create_timestamp()}.txt"
            )

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(secret)

            print("解析成功～")
            print(secret)
            print(f"\n保存先: {output_file}")
            input(
                "\n成功しました。QRコードも、秘密鍵テキストも、"
                "他の人に見えないようにしましょう！！"
            )
            return

    #QRコード全体の読み取り結果を出力
    base_name = f"[{image_path.name}]"

    output_file = (
        image_path.parent /
        f"qrDecode_{base_name}_{create_timestamp()}.txt"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(data)

    print("解析成功～")
    print(data)
    print(f"\n保存先: {output_file}")
    input("\n成功しました！Enterキーで終了！！")


if __name__ == "__main__":

    try:
        main()

    except Exception:
        error_text = traceback.format_exc()

        folder = (
            Path(sys.argv[1]).parent
            if len(sys.argv) >= 2
            else Path.cwd()
        )

        write_error(folder, error_text)

        input("\n失敗しました。Enterキーで終了...")
