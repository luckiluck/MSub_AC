import os
import re
import requests
from urllib.parse import quote

def get_kitsu_id(sub_dir, season=None):

    def clean_anime_name(name):
        name = re.sub(r'[^\w]', ' ', name).lower()
        return re.sub(r'\s+', ' ', name).strip()  # Replace multiple spaces with a single space and strip leading/trailing spaces
    # Get list of all srt files in sub_dir
    srt_files = [f for f in os.listdir(sub_dir) if f.endswith('.srt')]

    # Get anime name from sub_dir
    org_name = os.path.basename(sub_dir)
    anime_name = clean_anime_name(org_name)

    # Make GET request to https://kitsu.io/api/edge/anime?filter[text]={anime_name} to get anime_id
    print(f"[\033[95mInfo\033[0m] Making GET request to {f'https://kitsu.io/api/edge/anime?filter[text]={quote(anime_name)}'} ...")
    response = requests.get(
        'https://kitsu.io/api/edge/anime',
        params={'filter[text]': anime_name}
    )
    response.raise_for_status()

    anime_index = None
    for index, anime in enumerate(response.json()['data']):
        titles = anime['attributes'].get('titles', {})
        canonical_title = anime['attributes'].get('canonicalTitle', '')
        abbreviated_titles = anime['attributes'].get('abbreviatedTitles', [])

        stripped_titles = [
            clean_anime_name(titles.get('en_jp', '')),
            clean_anime_name(titles.get('ja_jp', '')),
            clean_anime_name(titles.get('en', '')),
            clean_anime_name(canonical_title),
            *map(clean_anime_name, abbreviated_titles)
        ]

        # Print the title retrieved from the API
        print(f"[\033[95mInfo\033[0m] Title en_jp: {titles.get('en_jp', '')}")
        print(f"[\033[95mInfo\033[0m] Title ja_jp: {titles.get('ja_jp', '')}")
        print(f"[\033[95mInfo\033[0m] Title en: {titles.get('en', '')}")
        print(f"[\033[95mInfo\033[0m] Canonical Title: {canonical_title}")
        print(f"[\033[95mInfo\033[0m] Abbreviated Titles: {abbreviated_titles}\n")

        # Compare stripped anime_name with stripped titles
        if anime_name in stripped_titles:
            anime_index = index
            break

    if anime_index is None:
        print(f"[\033[91mError\033[0m] No matching anime found for '{anime_name}'.")
        return None

    if season:
        print(f"[\033[95mInfo\033[0m] Getting Kitsu ID for {org_name} season {season}...")
        for index, anime in enumerate(response.json()['data']):
            episodes = requests.get(
                f'https://kitsu.io/api/edge/anime/{anime["id"]}/episodes'
            )
            episodes.raise_for_status()
            if season == episodes.json()['data'][0]['attributes']['seasonNumber']:
                anime_index = index
                break

    anime_episodes = response.json()['data'][anime_index]['attributes']['episodeCount']

    # If the number of .srt files in the sub_dir is different from the number of episodes, raise an error
    if len(srt_files) != anime_episodes:
        raise ValueError(f"[\033[91mError\033[0m] Number of episodes ({anime_episodes}) does not match number of .srt files ({len(srt_files)}) in {sub_dir}")

    anime_id = response.json()['data'][anime_index]['id']
    anime_title = response.json()['data'][anime_index]['attributes']['canonicalTitle']
    anime_desc = response.json()['data'][anime_index]['attributes']['synopsis']

    print(f"\033[94mAnime ID:\033[0m {anime_id}, \033[94mTitle:\033[0m {anime_title}, \033[94mEpisodes:\033[0m {anime_episodes}")
    print(f"\033[94mDescription:\033[0m {anime_desc}\n")

    return anime_id, anime_title


# Example usage
#sub_dir = 'D:\Python\MSub_AC\Japanese_Subtitles\THE IDOLM@STER Cinderella Girls'
#get_kitsu_id(sub_dir)