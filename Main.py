import json
import random
import re

import requests


class KuGouMusic:
    def __init__(self):
        self._headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Referer': 'https://www.kugou.com/',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 ('
                          'KHTML, like Gecko) Mobile/17D50 UCBrowser/12.8.2.1268 Mobile AliApp(TUnionSDK/0.1.20.3) '
        }

    def search_music(self, music_name, limit=30):
        return json.loads(requests.get(
            url='https://mobiles.kugou.com/api/v3/search/song?format=jsonp&keyword={}&pagesize={}'.format(music_name,
                                                                                                          limit),
            headers=self._headers).text.replace('(', '').replace(')', ''))['data']['info']

    def get_music_info(self, music_hash_id, music_album_id):
        return requests.get(
            url='https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}&album_id={}'.format(music_hash_id,
                                                                                                  music_album_id),
            headers=self._headers,
            cookies={'kg_mid': ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 32)),
                     'kg_dfid': ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 24)),
                     'kg_dfid_collect': ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 32)),
                     'kg_mid_temp': ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 32))}
        ).json()

    def get_playlist_info(self, list_id):
        html = requests.get(
            url='https://www.kugou.com/yy/special/single/{}.html'.format(list_id),
            headers=self._headers).text
        music_name = re.findall('<li><a title="(.*?)" hidefocus', html)
        music_url = re.findall('href="(.*?)" data="', html)
        ret = {'id': list_id,
               'list': []}
        for i in range(len(music_url)):
            ret['list'].append({
                'name': music_name[i],
                'url': music_url[i]
            })
        return json.dumps(ret)


if __name__ == "__main__":
    KGM = KuGouMusic()
    ret = KGM.search_music('起风了', 30)
    for i in range(len(ret)):
        name = ret[i]['songname']
        singer_name = ret[i]['singername']
        song_hash = ret[i]['hash']
        album_id = ret[i]['album_id']
        print('音乐名:{} 歌手名:{} 歌曲hash:{} album_id:{}'.format(name, singer_name, song_hash, album_id))
    ret = KGM.get_music_info('eb30fa0b0712a2c44a41d70188d909f9', '53218722')['data']
    music_url = ret['play_backup_url']
    song_name = ret['song_name']
    lyrics = ret['lyrics']
    author_name = ret['author_name']
    print('歌曲名:{} 歌手名:{} 音乐下载URL:{}\n歌词:{}'.format(song_name, author_name, music_url, lyrics))
