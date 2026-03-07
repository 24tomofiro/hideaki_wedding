import os
import subprocess
import random
import glob

# directories
base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, 'images')
bgm_dir = os.path.join(base_dir, 'bgm')
output_file = os.path.join(base_dir, 'slideshow.mp4')

# config
fps = 30
duration_per_image = 5 # seconds

def main():
    # 1. Get images
    images = []
    for ext in ['*.[jJ][pP][gG]', '*.[jJ][pP][eE][gG]', '*.[pP][nN][gG]']:
        images.extend(glob.glob(os.path.join(images_dir, ext)))
    images = sorted(images)

    if not images:
        print(f"エラー: 画像が {images_dir} フォルダに見つかりません。")
        return

    # 2. Get BGM
    bgm_files = glob.glob(os.path.join(bgm_dir, '*.[mM][pP]3')) + glob.glob(os.path.join(bgm_dir, '*.[wW][aA][vV]'))
    bgm_file = bgm_files[0] if bgm_files else None

    if bgm_file:
        print(f"BGM: {os.path.basename(bgm_file)} を使用します。")
    else:
        print("BGMが見つかりません。無音の動画を作成します。")

    print(f"合計 {len(images)} 枚の画像からスライドショーを作成します...")

    inputs = []
    filter_complex = []

    for i, img in enumerate(images):
        inputs.extend(['-i', img])
        frames = int(duration_per_image * fps)
        
        # Random Ken Burns effects
        effects = [
            # Zoom In Center
            f"zoompan=z='min(zoom+0.0015,1.5)':d={frames}:fps={fps}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080",
            # Zoom Out Center
            f"zoompan=z='max(1.3-0.002*on,1)':d={frames}:fps={fps}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080",
            # Pan Right
            f"zoompan=z='1.2':d={frames}:fps={fps}:x='max(1,iw/zoom-x-1)':y='ih/2-(ih/zoom/2)':s=1920x1080",
            # Pan Left
            f"zoompan=z='1.2':d={frames}:fps={fps}:x='x+1':y='ih/2-(ih/zoom/2)':s=1920x1080",
            # Pan Down
            f"zoompan=z='1.2':d={frames}:fps={fps}:x='iw/2-(iw/zoom/2)':y='max(1,ih/zoom-y-1)':s=1920x1080",
            # Pan Up
            f"zoompan=z='1.2':d={frames}:fps={fps}:x='iw/2-(iw/zoom/2)':y='y+1':s=1920x1080"
        ]
        
        selected_effect = random.choice(effects)
        
        # scale to fit 1920x1080 with black padding before zoompan to handle vertical images securely
        filter_complex.append(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,{selected_effect},format=yuv420p[v{i}];")

    # Concat all video streams
    concat_filter = "".join([f"[v{i}]" for i in range(len(images))])
    concat_filter += f"concat=n={len(images)}:v=1:a=0[outv_raw];"
    
    # Add fadeout at the end
    total_duration = len(images) * duration_per_image
    fade_duration = 2
    concat_filter += f"[outv_raw]fade=t=out:st={total_duration - fade_duration}:d={fade_duration}[outv]"
    
    filter_complex.append(concat_filter)
    
    cmd = [
        'ffmpeg', '-y',
        *inputs
    ]
    
    if bgm_file:
        cmd.extend(['-i', bgm_file])
    
    cmd.extend([
        '-filter_complex', "".join(filter_complex),
        '-map', '[outv]'
    ])
    
    if bgm_file:
        cmd.extend([
            '-map', f'{len(images)}:a',
            '-af', f'afade=t=out:st={total_duration - fade_duration}:d={fade_duration}',
            '-c:a', 'aac', '-b:a', '192k'
        ])
        
    cmd.extend([
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-t', str(total_duration), # Ensure it stops exactly after all images
        output_file
    ])

    print("実行コマンド:", " ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        print(f"成功: 動画が {output_file} に保存されました！")
    except subprocess.CalledProcessError as e:
        print("エラー: 動画の生成に失敗しました。")
        print(e)

if __name__ == "__main__":
    main()
