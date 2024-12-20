import random
import time

import requests
from db import DB
from loguru import logger

db = DB('music.db')


def get_song_list(url: str):
    data = {
        "url": url
    }
    content = requests.post(url="http://192.168.6.228:8081/songlist", data=data).json()
    assert content['code'] == 1, content['msg']
    return content['data']['songs']


def sync_song_list(song_list):
    # 反转歌单
    song_list.reverse()
    count = 0
    song_id = db.select_data('song_list', 'count(*)', '1=1')[0][0]
    for song in song_list:
        song_name, singer_name = song.split('-')[0], song.split('-')[1]
        song_name = song_name.strip()
        singer_name = singer_name.strip()
        if db.select_data('song_list', 'song_name', f'song_name="{song_name.strip()}" and singer_name="{singer_name}"'):
            logger.warning(f'{song_name} - {singer_name} 已存在')
            continue
        else:
            # logger.success(f'{song_name} - {singer_name} 正在下载')
            time.sleep(random.randint(2,3))
            logger.success(f'{song_name} - {singer_name} 下载完成')
            count += 1
        download_status = 0
        song_url = ''
        download_path = ''
        album_name = ''
        song_id = song_id + 1
        is_deleted = 0
        db.insert_data('song_list',
                       [song_id, song_name, singer_name, album_name, song_url, download_status, download_path,
                        is_deleted])
    logger.success(f'本次新增下载 {count} 首,合计 {song_id} 首')


if __name__ == '__main__':
    # db.create_table('song_list', ['song_id', 'song_name', 'singer_name', 'album_name', 'song_url', 'download_status',
    #                               'download_path'])
    url = 'https://c6.y.qq.com/base/fcgi-bin/u?__=o0ipIjwyesjT'
    song_list = get_song_list(url)
    sync_song_list(song_list)
