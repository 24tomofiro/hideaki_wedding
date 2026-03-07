import os
import subprocess
import random

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
    # Just pass the image once. zoompan will generate the duration.
    inputs.extend(['-i', os.path.join(assets_dir, img)])
    
    # Calculate zoompan duration correctly
    frames = int(duration_per_image * fps)
    
    # To avoid zoompan jitter, we scale the image up hugely before zoompan, giving it more pixels to interpolate.
    # Base size is 1920x1080. We scale it up by 4x to 7680x4320, pad it if needed, then zoompan back down to 1920x1080.
    effects = [
        # Zoom In Center
        f"zoompan=z='min(zoom+0.0015,1.5)':d={frames}:fps={fps}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080",
        # Zoom Out Center
        f"zoompan=z='max(1.3-0.002*on,1)':d={frames}:fps={fps}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080",
        # Pan Right
        f"zoompan=z='1.1':d={frames}:fps={fps}:x='(iw-iw/zoom)*(on/{frames})':y='ih/2-(ih/zoom/2)':s=1920x1080",
        # Pan Left
        f"zoompan=z='1.1':d={frames}:fps={fps}:x='(iw-iw/zoom)*(1-on/{frames})':y='ih/2-(ih/zoom/2)':s=1920x1080",
        # Pan Down
        f"zoompan=z='1.1':d={frames}:fps={fps}:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*(on/{frames})':s=1920x1080",
        # Pan Up
        f"zoompan=z='1.1':d={frames}:fps={fps}:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*(1-on/{frames})':s=1920x1080",
    ]
    effect = random.choice(effects)
    
    # Apply sub-pixel anti-jitter technique:
    # 1. Scale to oversized resolution (7680x4320) maintaining aspect ratio
    # 2. Pad to exact oversized resolution
    # 3. Apply zoompan effect which outputs to final 1920x1080 resolution
    filter_complex.append(f"[{i}:v]scale=7680:4320:force_original_aspect_ratio=decrease,pad=7680:4320:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,{effect},setsar=1,format=yuv420p[v{i}];")

# Concatenate all streams
concat_inputs = "".join([f"[v{i}]" for i in range(len(images))])
total_duration = len(images) * duration_per_image
# Add fade out for the last 2 seconds
fade_start = total_duration - 2
filter_complex.append(f"{concat_inputs}concat=n={len(images)}:v=1:a=0,format=yuv420p,fade=t=out:st={fade_start}:d=2[v]")
filter_string = "".join(filter_complex)

# Write filter string to a file to avoid command line length limits
filter_script_path = "filter.txt"
with open(filter_script_path, "w", encoding="utf-8") as f:
    f.write(filter_string)

# Add BGM and loop it infinitely (-stream_loop -1) until the video stops
inputs.extend(['-stream_loop', '-1', '-i', bgm_file])

cmd = [
    'ffmpeg',
    '-y',
] + inputs + [
    '-filter_complex_script', filter_script_path,
    '-map', '[v]',
    '-map', f'{len(images)}:a',
    '-c:v', 'libx264',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-af', f'afade=t=out:st={fade_start}:d=2',
    '-t', str(total_duration), # Stop audio when video ends
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
