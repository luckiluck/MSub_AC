import os
import re
import requests


def get_kitsu_id(sub_dir):

    # Get anime name from sub_dir by extracting characters not inside [] or ()
    anime_name = os.path.basename(sub_dir)
    anime_name = re.sub(r'\[.*?\]|\(.*?\)', '', anime_name)

    # Make GET request to https://kitsu.io/api/edge/anime?filter[text]={anime_name} to get anime_id
    response = requests.get(
        'https://kitsu.io/api/edge/anime',
        params={'filter[text]': anime_name}
    )

    response.raise_for_status()

    anime_episodes = response.json()['data'][0]['attributes']['episodeCount']
    # If the number of .srt files in the sub_dir is different from the number of episodes, raise an error
    srt_files = [f for f in os.listdir(sub_dir) if f.endswith('.srt')]
    if len(srt_files) != anime_episodes:
        raise ValueError(f"Number of episodes ({anime_episodes}) does not match number of .srt files ({len(srt_files)}) in {sub_dir}")

    anime_id = response.json()['data'][0]['id']
    anime_title = response.json()['data'][0]['attributes']['canonicalTitle']
    anime_desc = response.json()['data'][0]['attributes']['synopsis']

    print(f"\033[94mAnime ID:\033[0m {anime_id}, \033[94mTitle:\033[0m {anime_title}, \033[94mEpisodes:\033[0m {anime_episodes}")
    print(f"\033[94mDescription:\033[0m {anime_desc}")

    return anime_id


# Example usage
#sub_dir = 'C:\AC\Working on\Github\MSub_AC\Japanese_Subtitles\Mobile Suit Gundam SEED - HD Remaster (01-48) (Webrip)'
#get_kitsu_id(sub_dir)