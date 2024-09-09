import os
from glob import glob,escape
from pyasstosrt import Subtitle

def convert_ass_to_srt(input_file, output_file):
    subtitle = Subtitle(input_file)
    subtitle.export(output_file)

def main():
    input_dir = input("Enter the directory containing .ass files: ")
    output_dir = input("Enter the directory to save .srt files: ")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_dir = input_dir.replace('\\', '\\\\')
    ass_files = glob(escape(input_dir) + '\\*.ass', recursive=True)

    for ass_file in ass_files:
        base_name = os.path.basename(ass_file)
        srt_file = os.path.join(output_dir, base_name.replace('.ass', '.srt'))
        convert_ass_to_srt(ass_file, output_dir)
        print(f"Converted {base_name} to {os.path.basename(srt_file)}")

if __name__ == "__main__":
    main()