import os
import re
import yaml
from urllib.parse import quote, urljoin

def extract_season_episode(filename):
    match = re.search(r'S(\d+)E(\d+)', filename)
    if match:
        return int(match.group(1)), int(match.group(2))

    match = re.search(r'(?:\s|-_|\[|第)(\d{1,3})(?:\s|_|v|\]|話)', filename)
    if match:
        return None, int(match.group(1))
    return None, None

def url_encode_path(path):
    # Convert backslashes to forward slashes and encode
    path = path.replace('\\', '/')
    return quote(path)

def generate_yaml(base_directory, base_url):
    seasons = {}
    for filename in os.listdir(base_directory):
        if filename.endswith('.srt'):
            season, episode = extract_season_episode(filename)
            if episode is not None:
                if season is not None:
                    if season not in seasons:
                        seasons[season] = []

                    # Use os.path.join for the relative path, then replace backslashes
                    relative_path = os.path.join(os.path.basename(base_directory), filename).replace('\\', '/')
                    encoded_path = url_encode_path(relative_path)
                    print(encoded_path)

                    seasons[season].append({
                        'path': encoded_path,
                        'episode': episode,
                        #'delay': -1.00  # Default delay, you can adjust this as needed
                    })
                else:
                    if 'Unknown' not in seasons:
                        seasons['Unknown'] = []

                    # Use os.path.join for the relative path, then replace backslashes
                    relative_path = os.path.join(os.path.basename(base_directory), filename).replace('\\', '/')
                    encoded_path = url_encode_path(relative_path)
                    print(encoded_path)

                    seasons['Unknown'].append({
                        'path': encoded_path,
                        'episode': episode,
                        #'delay': -1.00  # Default delay, you can adjust this as needed
                    })
            else:
                print(f"Skipping file: {filename}")

    for season_dir in os.listdir(base_directory):
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
                            if 'Unknown' not in seasons:
                                seasons['Unknown'] = []

                            # Use os.path.join for the relative path, then replace backslashes
                            relative_path = os.path.join(season_dir, filename).replace('\\', '/')
                            encoded_path = url_encode_path(relative_path)

                            seasons['Unknown'].append({
                                'path': encoded_path,
                                'episode': episode,
                                #'delay': -1.00  # Default delay, you can adjust this as needed
                            })

    # Construct the full base_url by combining it with the encoded base_directory
    encoded_base_dir = url_encode_path(os.path.basename(base_directory))
    full_base_url = urljoin(base_url, encoded_base_dir + '/')

    yaml_data = {
        'msubtitles': [{
            'source': full_base_url,
            'subtitles': [
                {
                    'season': season,
                    'items': sorted(items, key=lambda x: x['episode'])
                } for season, items in sorted(seasons.items())
            ]
        }]
    }

    return yaml.dump(yaml_data, sort_keys=False, allow_unicode=True)


# Example usage
base_directory = 'C:\AC\Working on\Github\MSub_AC\Japanese_Subtitles\White Album 2 - Re-timed for UTW BDs [01.26.17]'  # Replace with your actual base directory path
base_url = 'https://raw.githubusercontent.com/luckiluck/MSub_AC/main/Japanese_Subtitles/'  # Replace with your actual base URL
yaml_content = generate_yaml(base_directory, base_url)

with open('subtitles.yaml', 'w', encoding='utf-8') as f:
    f.write(yaml_content)

print("YAML file generated successfully.")