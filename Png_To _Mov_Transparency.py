import os
import subprocess
from PIL import Image

# 入力フォルダと出力フォルダの設定
input_folder = "frames"  # PNGフレームが保存されているフォルダ
transparent_folder = "frames_transparent"  # 透過済みPNGを保存するフォルダ
output_file = "output.mov"  # 出力するMOVファイル名

# フレームレート設定（必要に応じて調整可能）
frame_rate = 30

# 透過対象の色を指定（黒色: RGB = 0, 0, 0）
target_color = (0, 0, 0)

# 許容誤差（色の近似範囲を設定）
tolerance = 50

# 出力フォルダが存在しない場合は作成
if not os.path.exists(transparent_folder):
    os.makedirs(transparent_folder)

# 指定した色を透過する関数
def make_color_transparent(input_path, output_path, color, tolerance):
    # 画像を読み込み
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    # 新しいピクセルデータを作成
    new_data = []
    for item in datas:
        # 色の近似範囲で透過処理
        if abs(item[0] - color[0]) <= tolerance and \
           abs(item[1] - color[1]) <= tolerance and \
           abs(item[2] - color[2]) <= tolerance:
            new_data.append((0, 0, 0, 0))  # 完全に透明化
        else:
            new_data.append(item)

    # 新しいデータを画像に適用して保存
    img.putdata(new_data)
    img.save(output_path, "PNG")

# フォルダ内の全てのPNGファイルを処理
def process_frames(input_folder, transparent_folder, target_color, tolerance):
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(transparent_folder, filename)
            make_color_transparent(input_path, output_path, target_color, tolerance)
            print(f"Processed: {filename}")

# FFmpegコマンドを作成
def generate_mov(input_folder, output_file, frame_rate):
    # 入力ファイルパターン（連番PNGファイルの形式に合わせる）
    input_pattern = os.path.join(input_folder, "frame-%05d.png")
    
    # FFmpegコマンドを構築
    command = [
        "ffmpeg",
        "-r", str(frame_rate),  # フレームレート
        "-i", input_pattern,   # 入力ファイルパターン
        "-c:v", "prores_ks",   # コーデック（ProRes 4444を使用）
        "-profile:v", "4444",  # ProRes 4444プロファイル（アルファチャンネル付き）
        "-pix_fmt", "yuva444p",  # ピクセルフォーマット（アルファ付き）
        output_file            # 出力ファイル
    ]
    
    # コマンドを実行
    try:
        print("FFmpegコマンドを実行中...")
        subprocess.run(command, check=True)
        print(f"動画が正常に作成されました: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"エラーが発生しました: {e}")
    except FileNotFoundError:
        print("FFmpegがインストールされていない可能性があります。インストールを確認してください。")

if __name__ == "__main__":
    # フレームの透過処理
    if not os.path.exists(input_folder):
        print(f"入力フォルダが見つかりません: {input_folder}")
    else:
        print("フレームの透過処理を開始します...")
        process_frames(input_folder, transparent_folder, target_color, tolerance)
        print("透過処理が完了しました！")

    # MOV動画の生成
    if not os.path.exists(transparent_folder):
        print(f"透過フォルダが見つかりません: {transparent_folder}")
    else:
        print("MOV動画の生成を開始します...")
        generate_mov(transparent_folder, output_file, frame_rate)
