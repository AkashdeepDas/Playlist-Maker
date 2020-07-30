from song_list import song_list
import requests
import bs4
import json
import re
from time import sleep

url = 'https://www.youtube.com/results?search_query='
pattern = re.compile(r'window\["ytInitialData"\]')
url_list = []
i = 0

for song in song_list:
    i = i + 1
    try:
        data = requests.get(url + song.replace(' ', '+'))
        sleep(1)
        soup = bs4.BeautifulSoup(data.text, 'lxml')

        script = soup.find('script', string=pattern)
        info_dict = json.loads(str(script).split(
            ';')[0].split(' = ', maxsplit=1)[1])

        tabs = info_dict['contents']['twoColumnSearchResultsRenderer']['primaryContents']
        section_content = tabs['sectionListRenderer']['contents']
        item_content = section_content[0]['itemSectionRenderer']['contents'][0]
        video_data = item_content['videoRenderer']

        print(str(i) + ' https://www.youtube.com/watch?v=' +
              video_data['videoId'])
        url_list.append('https://www.youtube.com/watch?v=' +
                        video_data['videoId'])

    except json.decoder.JSONDecodeError:
        print("Can't find " + str(i) + ' ' + song)
    except KeyError:
        print("Can't find " + str(i) + ' ' + song)

print('\n\n')
print(url_list)
