import os
import re
import yaml
from urllib.parse import quote, urljoin

from get_kitsu_id import get_kitsu_id

def extract_season_episode(filename):
    match = re.search(r'S(\d+)E(\d+)', filename)
    if match:
        return int(match.group(1)), int(match.group(2))

    season = None
    match = re.search(r'S(\d+)', filename)
    if match:
        season = int(match.group(1))

    episode = None
    match = re.search(r'E(\d+)', filename)
    if match:
        episode = int(match.group(1))

    match = re.search(r'(?:\s|-_|\[|第|_)(\d{2,3})(?:\s|_|v\d{1}|\]|話|\..{3})', filename)
    if match:
        return season if season is not None else None, int(match.group(1))

    return season, episode

def url_encode_path(path):
    # Convert backslashes to forward slashes and encode
    path = path.replace('\\', '/')
    return quote(path)

def generate_yaml(base_directory, base_url, kitsu_id=True):
    seasons = {}
    yaml_data = {}

    encoded_base_dir = url_encode_path(os.path.basename(base_directory))
    # Construct the full base_url by combining it with the encoded base_directory
    full_base_url = urljoin(base_url, encoded_base_dir + '/')

    for filename in os.listdir(base_directory):

        if filename.endswith('.srt'):
            season, episode = extract_season_episode(filename)
            if 'Unknown' not in seasons:
                seasons['Unknown'] = []

            # Use os.path.join for the relative path, then replace backslashes
            encoded_path = url_encode_path(filename)

            if episode is not None:
                seasons['Unknown'].append({
                    'path': encoded_path,
                    'episode': episode,
                    #'delay': -1.00  # Default delay, you can adjust this as needed
                })
            else:
                print(f"\033[95mMovie type file: {filename} or episode number not found.\033[0m\n")
                seasons['Unknown'].append({
                    'path': encoded_path,
                    'episode': 1,
                    #'delay': -1.00  # Default delay, you can adjust this as needed
                })

            yaml_data = {
                'msubtitles': [{
                    'source': full_base_url,
                    'subtitles': [
                        {
                            'season': season,
                            'items': sorted(seasons[season], key=lambda x: x['episode'])
                        } for season in seasons
                    ]
                }]
            }

    if yaml_data:
        print("\033[95mLink to generated YAML file:\033[0m")
        yaml_link = f'https://raw.githubusercontent.com/luckiluck/MSub_AC/main/Japanese_Subtitles/{encoded_base_dir}/{encoded_base_dir}.yaml'
        print(yaml_link)
        if len(yaml_link) > 200:
            print(f"\033[91mYAML file link is too long ({len(yaml_link)} characters)!\033[0m\n")

        # Get Kitsu ID
        if kitsu_id:
            anime_id = get_kitsu_id(base_directory)
            yaml_data['msubtitles'][0]['subtitles'][0]['season'] = int(anime_id)

        with open(f'{base_directory + "/" + os.path.basename(base_directory)}.yaml', 'w', encoding='utf-8') as f:
            f.write(yaml.dump(yaml_data, sort_keys=False, allow_unicode=True))
    else:
        print("No .srt files found in the specified directory.")

    for season_dir in os.listdir(base_directory):
        seasons = {}
        season_path = os.path.join(base_directory, season_dir)

        if os.path.isdir(season_path):

            for filename in os.listdir(season_path):
                if filename.endswith('.srt'):
                    season, episode = extract_season_episode(filename)
                    if episode is not None:
                        if season is not None:
                            if season not in seasons:
                                seasons[season] = []

                            # Use os.path.join for the relative path, then replace backslashes
                            relative_path = os.path.join(season_dir, filename).replace('\\', '/')
                            encoded_path = url_encode_path(relative_path)

                            seasons[season].append({
                                'path': encoded_path,
                                'episode': episode,
                                #'delay': -1.00  # Default delay, you can adjust this as needed
                            })
                        else:
                            print(f"Skipping file: {filename}")

            if seasons:
                print("\033[95mLink to generated YAML file:\033[0m")
                yaml_link = f'https://raw.githubusercontent.com/luckiluck/MSub_AC/main/Japanese_Subtitles/{encoded_base_dir}/{url_encode_path(season_dir)}/{url_encode_path(season_dir)}.yaml'
                print(yaml_link)
                if len(yaml_link) > 200:
                    print(f"\033[91mYAML file link is too long ({len(yaml_link)} characters)!\033[0m\n")

                # Get Kitsu ID
                anime_id = None
                if kitsu_id:
                    anime_id = get_kitsu_id(base_directory)

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

                with open(f'{base_directory + "/" + season_dir + "/" + season_dir}.yaml', 'w', encoding='utf-8') as f:
                    f.write(yaml.dump(yaml_data, sort_keys=False, allow_unicode=True))

    return


# Example usage
base_directory = 'D:\Python\MSub_AC\Japanese_Subtitles\Kage no Jitsuryokusha ni Naritakute！ 2nd Season'  # Replace with your actual base directory path
base_url = 'https://raw.githubusercontent.com/luckiluck/MSub_AC/main/Japanese_Subtitles/'  # Replace with your actual base URL
yaml_content = generate_yaml(base_directory, base_url)

print("\033[92mYAML file generated successfully.\033[0m")
