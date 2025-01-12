# STARTUP_MV

## Create_ShootingStar.pde

This Processing sketch generates an animation of shooting stars.

```processing
int frameCountLimit = 7500; // Output 7500 frames (equivalent to 4 minutes and 10 seconds)
int numShootingStars = 5; // Number of shooting stars
ShootingStar[] shootingStars; // Array to hold shooting stars

void setup() {
  size(1920, 1080, P2D); // Set the resolution to 16:9
  shootingStars = new ShootingStar[numShootingStars];
  for (int i = 0; i < numShootingStars; i++) {
    shootingStars[i] = new ShootingStar(); // Initialize each shooting star
  }
  frameRate(30); // Set the frame rate to 30fps
}

void draw() {
  background(0, 0, 0); // Set the background to black (RGB: 0, 0, 0)

  // Update and display each shooting star
  for (int i = 0; i < numShootingStars; i++) {
    shootingStars[i].update();
    shootingStars[i].display();
  }

  // Save frames
  if (frameCount <= frameCountLimit) {
    saveFrame("frames/frame-#####.png");
  } else {
    println("Frame saving completed");
    noLoop(); // Stop drawing when saving is complete
  }
}

// Shooting star class
class ShootingStar {
  float x, y;        // Position
  float speedX, speedY; // Velocity
  float length;      // Length of the shooting star
  float alpha;       // Transparency

  ShootingStar() {
    reset();
  }

  void reset() {
    x = random(width, width * 1.5); // Start from the right side of the screen
    y = random(-height * 0.5, height * 0.5); // Start randomly from the top
    speedX = random(-15, -20); // Move quickly to the left and down
    speedY = random(8, 12);
    length = random(80, 150); // Length of the shooting star
    alpha = 255; // Maximum transparency (opaque)
  }

  void update() {
    x += speedX;
    y += speedY;
    alpha -= 5; // Fade out

    // Reset if it goes off-screen
    if (x < -length || y > height || alpha <= 0) {
      reset();
    }
  }

  void display() {
    stroke(255, 255, 255, alpha); // White shooting star
    strokeWeight(2);
    line(x, y, x - length, y + length); // Draw the shooting star
  }
}
```

### Usage (English)

1. Open the `Create_ShootingStar.pde` file in the Processing IDE.
2. Ensure the resolution is set to 1920x1080 in the code (`size(1920, 1080, P2D);`).
3. Run the sketch. This will generate a series of PNG files in the `frames/` folder. The script is set to generate 7500 frames, which at 30fps is approximately 4 minutes and 10 seconds.

### Usage (Japanese)

1. Processing IDEで `Create_ShootingStar.pde` ファイルを開きます。
2. コード内の解像度が1920x1080に設定されていることを確認してください (`size(1920, 1080, P2D);`)。
3. スケッチを実行します。これにより、`frames/` フォルダに一連のPNGファイルが生成されます。スクリプトは7500フレームを生成するように設定されており、これは30fpsで約4分10秒です。

## Png_To _Mov_Transparency.py

This Python script converts a series of PNG frames with a black background to a transparent MOV video using FFmpeg.

```python
import os
import subprocess
from PIL import Image

# Input and output folder settings
input_folder = "frames"  # Folder where PNG frames are saved
transparent_folder = "frames_transparent"  # Folder to save transparent PNGs
output_file = "output.mov"  # Output MOV file name

# Frame rate setting (adjust if necessary)
frame_rate = 30

# Specify the color to make transparent (black: RGB = 0, 0, 0)
target_color = (0, 0, 0)

# Tolerance for color approximation
tolerance = 50

# Create the output folder if it doesn't exist
if not os.path.exists(transparent_folder):
    os.makedirs(transparent_folder)

# Function to make a specific color transparent
def make_color_transparent(input_path, output_path, color, tolerance):
    # Load the image
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    # Create new pixel data
    new_data = []
    for item in datas:
        # Apply transparency within the color tolerance
        if abs(item[0] - color[0]) <= tolerance and \
           abs(item[1] - color[1]) <= tolerance and \
           abs(item[2] - color[2]) <= tolerance:
            new_data.append((0, 0, 0, 0))  # Fully transparent
        else:
            new_data.append(item)

    # Apply the new data to the image and save
    img.putdata(new_data)
    img.save(output_path, "PNG")

# Process all PNG files in the folder
def process_frames(input_folder, transparent_folder, target_color, tolerance):
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(transparent_folder, filename)
            make_color_transparent(input_path, output_path, target_color, tolerance)
            print(f"Processed: {filename}")

# Create the FFmpeg command
def generate_mov(input_folder, output_file, frame_rate):
    # Input file pattern (match the sequence of PNG files)
    input_pattern = os.path.join(input_folder, "frame-%05d.png")

    # Build the FFmpeg command
    command = [
        "ffmpeg",
        "-r", str(frame_rate),  # Frame rate
        "-i", input_pattern,   # Input file pattern
        "-c:v", "prores_ks",   # Codec (using ProRes 4444)
        "-profile:v", "4444",  # ProRes 4444 profile (with alpha channel)
        "-pix_fmt", "yuva444p",  # Pixel format (with alpha)
        output_file            # Output file
    ]

    # Execute the command
    try:
        print("Executing FFmpeg command...")
        subprocess.run(command, check=True)
        print(f"Successfully created the video: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except FileNotFoundError:
        print("FFmpeg may not be installed. Please check your installation.")

if __name__ == "__main__":
    # Process the frames to add transparency
    if not os.path.exists(input_folder):
        print(f"Input folder not found: {input_folder}")
    else:
        print("Starting frame transparency processing...")
        process_frames(input_folder, transparent_folder, target_color, tolerance)
        print("Transparency processing complete!")

    # Generate the MOV video
    if not os.path.exists(transparent_folder):
        print(f"Transparent folder not found: {transparent_folder}")
    else:
        print("Starting MOV video generation...")
        generate_mov(transparent_folder, output_file, frame_rate)
```

### Usage: Converting PNG frames to transparent MOV (English)

1. **Generate PNG frames:** First, run the `Create_ShootingStar.pde` sketch in Processing. This will create a series of PNG files in the `frames/` folder.
2. **Run the Python script:** Execute the `Png_To _Mov_Transparency.py` script. Ensure you have Python installed along with the Pillow (PIL) library (`pip install Pillow`).
3. **Check for FFmpeg:** The script uses FFmpeg to create the MOV file. Make sure FFmpeg is installed and accessible in your system's PATH.
4. **Output:** The script will first process all PNG files in the `frames/` folder, making the black background transparent and saving the results in the `frames_transparent/` folder. Then, it will use FFmpeg to combine these transparent PNGs into a MOV file named `output.mov` in the same directory as the script.

### Usage: Converting PNG frames to transparent MOV (Japanese)

1. **PNGフレームを生成:** まず、Processingで `Create_ShootingStar.pde` スケッチを実行します。これにより、`frames/` フォルダに一連のPNGファイルが作成されます。
2. **Pythonスクリプトを実行:** `Png_To _Mov_Transparency.py` スクリプトを実行します。PythonとPillow (PIL)ライブラリ (`pip install Pillow`) がインストールされていることを確認してください。
3. **FFmpegの確認:** スクリプトはMOVファイルを作成するためにFFmpegを使用します。FFmpegがインストールされ、システムのPATHにアクセス可能であることを確認してください。
4. **出力:** スクリプトは最初に `frames/` フォルダ内のすべてのPNGファイルを処理し、黒色の背景を透明にして `frames_transparent/` フォルダに保存します。次に、FFmpegを使用してこれらの透明なPNGを結合し、スクリプトと同じディレクトリに `output.mov` という名前のMOVファイルを作成します。
