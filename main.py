import requests
import json
import logging

from kafka import KafkaProducer
from pprint import pprint
from constants import YOUTUBE_API_KEY, PLAYLIST_ID

def fetch_page(url, parameters, page_token=None):
    params = {**parameters, 'key': YOUTUBE_API_KEY, 'page_token': page_token}
    response = requests.get(url, params)
    payload = json.loads(response.text)

    return payload


def fetch_page_lists(url, parameters, page_token=None):
    while True:
        payload = fetch_page(url, parameters, page_token)
        yield from payload['items']

        page_token = payload.get('nextPageToken')
        if page_token is None:
            break

def format_response(video):
    video_metrics = {
        'title':video['snippet']['title'],
        'views': int(video['statistics']['viewCount']),
        'likes': int(video['statistics']['likeCount']),
        'comments': int(video['statistics']['commentCount']),
        'favorites': int(video['statistics']['favoriteCount']),
        'thumbnail': video['snippet']['thumbnails']['default']['url']
        }
    
    return video_metrics

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    # response =  requests.get("https://www.googleapis.com/youtube/v3/videos", 
    #                          {
    #                              'key': YOUTUBE_API_KEY,
    #                              'id': 'ArCnt4eAUAk',
    #                              'part': 'snippet,statistics,status'
    #                          })
    
    # # print(response.text)

    # response = json.loads(response.text)['items']

    # for item in response:
    #     video_metrics = {
    #         'title':item['snippet']['title'],
    #         'views': int(item['statistics']['viewCount']),
    #         'likes': int(item['statistics']['likeCount']),
    #         'comments': int(item['statistics']['commentCount']),
    #         'favorites': int(item['statistics']['favoriteCount']),
    #         'thumbnail': item['snippet']['thumbnails']['default']['url']
    #     }

    # print(pprint(video_metrics))

    for video_item in fetch_page_lists(
            "https://www.googleapis.com/youtube/v3/playlistItems",
            {'playlistId': PLAYLIST_ID, 'part': 'snippet,contentDetails'},
            None):
        video_id = video_item['contentDetails']['videoId']

        for video in fetch_page_lists(
                "https://www.googleapis.com/youtube/v3/videos",
                {'id': video_id, 'part': 'snippet,statistics'},
                None):
            # logging.info("Video here => %s", pprint(format_response(video)))

            producer.send('youtube_videos', json.dumps(format_response(video)).encode('utf-8'),
                          key=video_id.encode('utf-8'))
            print('Sent', video['snippet']['title'])
            # producer.flush()

    # response =  requests.get("https://www.googleapis.com/youtube/v3/playlistItems", 
    #                              {
    #                                  'key': YOUTUBE_API_KEY,
    #                                  'playlistId': PLAYLIST_ID,
    #                                  'part': 'snippet,contentDetails,status',
    #                                  'nextPageToken': 'EAAajQFQVDpDQVVpRUVRME5UaERRemhFTVRFM016VXlOeklvQVVpZXBLLUVvZWlKQTFBQldrUWlRMmxLVVZSSGVGZGlTR3hJVm01U01tUldXbk5YYldjeFVsWnNXVmRWU25OTlYwWjJUbXhHZFdSc1drWmhWMDVzUldkelNUTXRVSGgxVVZsUmMwbzJlbGRSSWc' 
    #                              })
    
    # print(response.text)