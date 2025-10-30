import numpy as np
import cv2


class MyVideoCapture:
    """Webカメラから映像を取得し、保存するクラス。

    Attributes:
        cap (cv2.VideoCapture): OpenCVのビデオキャプチャオブジェクト。
        captured_img (np.ndarray | None): 最後にキャプチャされた画像データ。
    """

    DELAY: int = 100  # 100 msecのディレイ

    def __init__(self) -> None:
        """Webカメラを初期化する。

        Notes:
            PCによってはカメラIDが0ではなく1で動作する場合があるため、
            必要に応じて cv2.VideoCapture(1) に変更すること。
        """
        self.cap: cv2.VideoCapture = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.captured_img: np.ndarray | None = None

    def run(self) -> None:
        """カメラ画像を１枚キャプチャする"""
        ret,frame = self.cap.read()
        if ret:
            self.captured_img = frame 
        else:
            print("カメラから画像を取得できませんでした。")

    def replace_white_with_camera(self, base_img_path: str='google.png', save_path: str = 'output_images/merged.png') -> None:
        """白色部分をカメラ画像で置き換える。
        Args:
            base_img_path (str): 白を置換するベース画像のパス。
            save_path (str, optional): 保存先のファイルパス。デフォルトは 'output_images/merged.png'。
        Raises:
            ValueError: キャプチャ画像が存在しない場合。
            FileNotFoundError: ベース画像が存在しない場合。
        """
        if self.captured_img is None:
            raise ValueError("キャプチャ画像が存在しません。run()を実行してください。")

        # ベース画像を読み込む
        base_img = cv2.imread(base_img_path)
        if base_img is None:
            raise FileNotFoundError(f"ベース画像 '{base_img_path}' が見つかりません。")

        # カメラ画像をベース画像と同じサイズにリサイズ
        cam_img = cv2.resize(self.captured_img, (base_img.shape[1], base_img.shape[0]))

        # 行数・列数を取得
        rows, cols, _ = base_img.shape

        # 画素ごとに走査して白色部分を置換
        for y in range(rows):
            for x in range(cols):
                b, g, r = base_img[y, x]
                # 白または白に近い部分を検出（ある程度の閾値を設定）
                if b > 240 and g > 240 and r > 240:
                    # 白い部分をカメラ画像の対応ピクセルで置換
                    base_img[y, x] = cam_img[y, x]

        # 保存ディレクトリが存在しない場合は作成
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 画像を保存
        cv2.imwrite(save_path, base_img)
        print(f"白色部分をカメラ画像で置き換えた画像を {save_path} に保存しました。")


def k24008():
    """main.py から呼び出すための関数"""
    app = MyVideoCapture()
    app.run()
    app.replace_white_with_camera("images/google.png", "output_images/lecture05_01_k24008.png")