import os
import re
import requests


def get_kitsu_id(sub_dir, season=None):
    if season is None:
        # Get list of all srt files in sub_dir
        srt_files = [f for f in os.listdir(sub_dir) if f.endswith('.srt')]
        if len(srt_files) > 1:
            season = 1

    # Get anime name from sub_dir by extracting characters not inside [] or ()
    anime_name = os.path.basename(sub_dir)
    anime_name = re.sub(r'\[.*?\]|\(.*?\)', '', anime_name)

    # Make GET request to https://kitsu.io/api/edge/anime?filter[text]={anime_name} to get anime_id
    response = requests.get(
        'https://kitsu.io/api/edge/anime',
        params={'filter[text]': anime_name}
    )

    response.raise_for_status()
    anime_index = 0
    if season:
        print(f"Getting Kitsu ID for {anime_name} season {season}...")
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
        raise ValueError(f"Number of episodes ({anime_episodes}) does not match number of .srt files ({len(srt_files)}) in {sub_dir}")

    anime_id = response.json()['data'][anime_index]['id']
    anime_title = response.json()['data'][anime_index]['attributes']['canonicalTitle']
    anime_desc = response.json()['data'][anime_index]['attributes']['synopsis']

    print(f"\033[94mAnime ID:\033[0m {anime_id}, \033[94mTitle:\033[0m {anime_title}, \033[94mEpisodes:\033[0m {anime_episodes}")
    print(f"\033[94mDescription:\033[0m {anime_desc}\n")

    return anime_id


# Example usage
#sub_dir = 'D:\Python\MSub_AC\Japanese_Subtitles\THE IDOLM@STER Cinderella Girls'
#get_kitsu_id(sub_dir)