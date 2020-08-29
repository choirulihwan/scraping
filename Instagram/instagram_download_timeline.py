# instagram download media berdasar profile
# input adalah id yg didapatkan setelah diakses

import os
import requests, json, time

url1 = 'https://www.instagram.com/graphql/query/'

profile = input('Please enter profile: ')
count = 0
end_cursor = ''
query_hash = 'bfa387b2992c3a52dcbe447467b4b771'

# create folder
try:
    os.makedirs('media_timeline/{}'.format(profile))
except OSError as e:
    print("create dir failed")

while True:
    variables = {
        "id": profile,
        "first": 50,
        'after': end_cursor
    }

    params = {
        'query_hash': query_hash,
        'variables': json.dumps(variables),

    }

    response = requests.get(url1, params=params).json()
    try:
        users = response['data']['user']['edge_owner_to_timeline_media']['edges']
    except:
        print("wait for 30 seconds..")
        time.sleep(30)
        continue
        # continue akan mengembalikan posisi eksekusi script ke variables

    for user in users:
        post_id = user['node']['id']

        count += 1
        print(count, post_id)

        is_video = user['node']['is_video']
        if is_video == True:
            filename = "{} {}.mp4".format(count, post_id)
            url_media = user['node']['video_url']
        else:
            filename = "{} {}.jpg".format(count, post_id)
            url_media = user['node']['display_url']

        path = 'media_timeline/{}/{}'.format(profile, filename)
        r_url_media = requests.get(url_media).content
        open(path, 'wb').write(r_url_media)
    end_cursor = response['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    has_next = response['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

    if has_next == False: break
    time.sleep(2)