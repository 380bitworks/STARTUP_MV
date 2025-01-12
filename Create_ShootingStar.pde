int frameCountLimit = 7500; // 7500フレーム（4分10秒分）を出力
int numShootingStars = 5; // 流れ星の数
ShootingStar[] shootingStars; // 流れ星の配列

void setup() {
  size(1920, 1080, P2D); // 解像度を16:9に設定
  shootingStars = new ShootingStar[numShootingStars];
  for (int i = 0; i < numShootingStars; i++) {
    shootingStars[i] = new ShootingStar(); // 各流れ星を初期化
  }
  frameRate(30); // フレームレートを30fpsに設定
}

void draw() {
  background(0, 0, 0); // 背景を黒色に設定（RGB: 0, 0, 0）

  // 各流れ星を更新・描画
  for (int i = 0; i < numShootingStars; i++) {
    shootingStars[i].update();
    shootingStars[i].display();
  }

  // フレームを保存
  if (frameCount <= frameCountLimit) {
    saveFrame("frames/frame-#####.png");
  } else {
    println("フレームの保存が完了しました");
    noLoop(); // 保存が完了したら描画を停止
  }
}

// 流れ星クラス
class ShootingStar {
  float x, y;        // 位置
  float speedX, speedY; // 移動速度
  float length;      // 流れ星の長さ
  float alpha;       // 透明度

  ShootingStar() {
    reset();
  }

  void reset() {
    x = random(width, width * 1.5); // 画面右外からスタート
    y = random(-height * 0.5, height * 0.5); // 上の方からランダムにスタート
    speedX = random(-15, -20); // 速いスピードで左下に移動
    speedY = random(8, 12);
    length = random(80, 150); // 流れ星の長さ
    alpha = 255; // 最大透明度
  }

  void update() {
    x += speedX;
    y += speedY;
    alpha -= 5; // 徐々に消える

    // 画面外に出たらリセット
    if (x < -length || y > height || alpha <= 0) {
      reset();
    }
  }

  void display() {
    stroke(255, 255, 255, alpha); // 白い流れ星
    strokeWeight(2);
    line(x, y, x - length, y + length); // 流れ星を描画
  }
}
