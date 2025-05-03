import os
import yaml
from urllib.parse import urljoin

from get_kitsu_id import get_kitsu_id
from utils import load_config
from utils import extract_season_episode, url_encode_path

def generate_yaml(base_directory, base_url, kitsu_id=True):
    def process_season_files(season_path, season_dir=None):
        seasons = {}
        for filename in os.listdir(season_path):
            if filename.endswith('.srt'):
                season, episode = extract_season_episode(filename)
                if episode is not None:
                    if season not in seasons:
                        seasons[season] = []

                    relative_path = os.path.join(season_dir, filename).replace('\\', '/') if season_dir else filename
                    encoded_path = url_encode_path(relative_path)

                    seasons[season].append({
                        'path': encoded_path,
                        'episode': episode,
                        # 'delay': -1.00  # Default delay, you can adjust this as needed
                    })
                else:
                    print(f"Skipping file: {filename}")
            else:
                print(f"[\033[93mWarning\033[0m] Skipping non-SRT file: {filename}")

        if not seasons and not os.path.basename(season_path) == "ass":
            print(f"[\033[91mError\033[0m] No SRT files found in {season_path}.")
            return None

        return seasons

    def generate_yaml_data(seasons, output_path, anime_id=None):
        yaml_data = {
            'msubtitles': [{
                'source': full_base_url,
                'subtitles': [
                    {
                        'season': int(anime_id) if anime_id is not None else season,
                        'items': sorted(items, key=lambda x: x['episode'])
                    } for season, items in sorted(seasons.items())
                ]
            }]
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(yaml.dump(yaml_data, sort_keys=False, allow_unicode=True))

    base_dir = os.path.basename(base_directory)
    encoded_base_dir = url_encode_path(os.path.basename(base_dir))
    if not base_url.endswith('/'):
        base_url += '/'
    full_base_url = urljoin(base_url, encoded_base_dir) + '/'

    # Process files in the base directory
    seasons = process_season_files(base_directory)
    max_link_length = int(load_config().get("max_yaml_link_length"))
    if seasons:
        season_info = f"S{max(seasons.keys())}" if len(seasons) == 1 else encoded_base_dir
        yaml_file_name = base_dir + '.yaml'
        yaml_link = f'{base_url}{encoded_base_dir}/{url_encode_path(yaml_file_name)}'
        if len(yaml_link) > max_link_length:
            yaml_file_name = f'{season_info}.yaml'
            print(f"[\033[93mWarning\033[0m] YAML file link is too long ({len(yaml_link)} characters (>{max_link_length}))!")
            print(f"[\033[95mInfo\033[0m] Shorten it to {yaml_file_name}")
            yaml_link = f'{base_url}{encoded_base_dir}/{url_encode_path(yaml_file_name)}'
            print(f"[\033[95mInfo\033[0m] New link has {len(yaml_link)} characters.")

        print("\n[\033[95mInfo\033[0m] Link to generated YAML file:\n", yaml_link)
        print("[\033[95mInfo\033[0m] Yaml file path: \n", os.path.join(base_directory, yaml_file_name), "\n")

        anime_id, anime_title = get_kitsu_id(base_directory, season=max(seasons.keys())) if kitsu_id else None
        if anime_id:
            output_path = f'{base_directory}/{yaml_file_name}'
            generate_yaml_data(seasons, output_path, anime_id)
        else:
            print("[\033[91mError\033[0m] Failed to get Kitsu ID.")
            return 1

    # Process subdirectories as seasons
    for season_dir in os.listdir(base_directory):
        season_path = os.path.join(base_directory, season_dir)
        if os.path.isdir(season_path):
            seasons = process_season_files(season_path, season_dir)
            if seasons:
                yaml_file_name = f'{season_dir}.yaml'
                yaml_link = f'{base_url}{encoded_base_dir}/{url_encode_path(season_dir)}/{url_encode_path(yaml_file_name)}'
                if len(yaml_link) > max_link_length:
                    yaml_file_name = f'S{max(seasons.keys())}.yaml'
                    yaml_link = f'{base_url}{encoded_base_dir}/{url_encode_path(season_dir)}/{url_encode_path(yaml_file_name)}'

                print("\n[\033[95mInfo\033[0m] Link to generated YAML file:\n", yaml_link)
                print("[\033[95mInfo\033[0m] Yaml file path: \n", os.path.join(season_path, yaml_file_name), "\n")
                if len(yaml_link) > 200:
                    print(f"[\033[93mWarning\033[0m] YAML file link is too long ({len(yaml_link)} characters (>{max_link_length}))!")
                print("\n")

                anime_id = get_kitsu_id(season_path, season=max(seasons.keys())) if kitsu_id else None
                if anime_id:
                    output_path = f'{base_directory}/{season_dir}/{yaml_file_name}'
                    generate_yaml_data(seasons, output_path, anime_id)
                else:
                    print("[\033[91mError\033[0m] Failed to get Kitsu ID.")
                    return 1

    return anime_title, anime_id, yaml_link


# Example usage
#base_directory = 'D:\Python\MSub_AC\Japanese_Subtitles\Kidou Senshi Zeta Gundam'  # USE OFFICIAL ANIME NAME FROM KITSU.IO!!!
#base_url = 'https://raw.githubusercontent.com/luckiluck/MSub_AC/main/Japanese_Subtitles/'  # Replace with your actual base URL
#yaml_content = generate_yaml(base_directory, base_url)
#
#if yaml_content:
#    print("\033[92mYAML file generated successfully.\033[0m")
#    print("\033[94mAnime Title:\033[0m", yaml_content[0])
#    print("\033[94mSeason:\033[0m", yaml_content[1])
#    print("\033[94mYAML Link:\033[0m", yaml_content[2])
