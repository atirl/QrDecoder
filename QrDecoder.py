#============================================================
# QrDecoder : QRコードテキスト化ツール
# 2023/06/11 atirl　作成
# 2026/10/21 atirl　日本語ファイル対応、exe化対応
# > python QrDecorder.py imagefile.jpg　でもいいですし
# 当ファイル.exeにQR画像ファイルをドラッグしてもいいです
# ※「画像ファイルと同じフォルダ」に出力されます
#============================================================
import sys
import traceback
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np

def create_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

#やっぱりエラーの場合もテキスト出力する
def write_error(folder, message):
    filename = folder / f"qrFailed_{create_timestamp()}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(message)

    print(message)
    print(f"\nエラーログ出力: {filename}")


def main():

    if len(sys.argv) < 2:
        raise Exception("QRコード画像をドラッグしてください。")

    image_file = sys.argv[1]
    image_path = Path(image_file)

    #日本語ファイル名対応
    img = cv2.imdecode(
        np.fromfile(image_file, dtype=np.uint8),
        cv2.IMREAD_COLOR
    )

    if img is None:
        raise Exception(
            f"画像を開けません……\n\nファイル:\n{image_file}"
        )

    detector = cv2.QRCodeDetector()

    data, points, _ = detector.detectAndDecode(img)

    if not data:
        raise Exception("QRコードが検出できませんでした。画像から。")

    #出力ファイル名
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
        