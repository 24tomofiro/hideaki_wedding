import os
import subprocess

assets_dir = r"C:\Users\24tom\workspace\hideaki\assets"
bgm_file = r"C:\Users\24tom\workspace\hideaki\オルゴールスキマスイッチ  全力少年.mp3"
output_file = r"C:\Users\24tom\workspace\hideaki\slideshow.mp4"

# Get all jpgs
images = [f for f in os.listdir(assets_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Create a complex filter for Ken Burns (zoom/pan)
# This will zoom each image in slowly.
duration_per_image = 5
fps = 30
transition_duration = 1

inputs = []
filter_complex = []

for i, img in enumerate(images):
    inputs.extend(['-loop', '1', '-t', str(duration_per_image), '-i', os.path.join(assets_dir, img)])
    
    # Scale and crop to 1920x1080 to maintain aspect ratio, then zoompan
    # zoompan formula: min(zoom+0.0015,1.5)
    filter_complex.append(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,format=yuv420p,zoompan=z='min(zoom+0.0015,1.5)':d={duration_per_image*fps}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080,setsar=1,format=yuv420p[v{i}];")

# Concatenate all streams
concat_inputs = "".join([f"[v{i}]" for i in range(len(images))])
filter_complex.append(f"{concat_inputs}concat=n={len(images)}:v=1:a=0,format=yuv420p[v]")
filter_string = "".join(filter_complex)

# Write filter string to a file to avoid command line length limits
filter_script_path = "filter.txt"
with open(filter_script_path, "w", encoding="utf-8") as f:
    f.write(filter_string)

# Add BGM
inputs.extend(['-i', bgm_file])

cmd = [
    'ffmpeg',
    '-y',
] + inputs + [
    '-filter_complex_script', filter_script_path,
    '-map', '[v]',
    '-map', f'{len(images)}:a',
    '-c:v', 'libx264',
    '-c:a', 'aac',
    '-shortest',
    '-pix_fmt', 'yuv420p',
    output_file
]

print("Running FFmpeg to generate video... This might take a few minutes depending on the PC speed.")
try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='cp932', errors='replace')
    print(f"Video generated at {output_file}")
except subprocess.CalledProcessError as e:
    print("FFmpeg failed with error:")
    print(e.stderr)
