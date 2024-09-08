import os
import re
from glob import glob

def ass_to_srt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    subtitle_lines = []
    for line in lines:
        if line.startswith('Dialogue:'):
            subtitle_lines.append(line)

    srt_lines = []
    for i, line in enumerate(subtitle_lines, 1):
        parts = line.split(',')
        start_time = parts[1].strip()
        end_time = parts[2].strip()
        text = ','.join(parts[9:]).strip()

        # Convert time format
        start_time = convert_time(start_time)
        end_time = convert_time(end_time)

        # Remove ASS tags
        text = re.sub(r'\{.*?\}', '', text)

        srt_lines.append(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(srt_lines)

def convert_time(time_str):
    h, m, s = time_str.split(':')
    s, ms = s.split('.')
    return f"{h}:{m}:{s},{ms[:3]}"

def main():
    input_dir = input("Enter the directory containing .ass files: ")
    output_dir = input("Enter the directory to save .srt files: ")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ass_files = glob(os.path.join(input_dir, '*.ass'))

    for ass_file in ass_files:
        base_name = os.path.basename(ass_file)
        srt_file = os.path.join(output_dir, base_name.replace('.ass', '.srt'))
        ass_to_srt(ass_file, srt_file)
        print(f"Converted {base_name} to {os.path.basename(srt_file)}")

if __name__ == "__main__":
    main()