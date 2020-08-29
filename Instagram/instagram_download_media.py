import os
import requests

hashtag = input('Please enter hashtag: ')
count = 0
end_cursor = ''

# create folder
try:
    os.makedirs('media_download/{}'.format(hashtag))
except OSError as e:
    print("create dir failed")

while True:
    url1 = 'https://www.instagram.com/explore/tags/{}/?__a=1&max_id={}'.format(hashtag, end_cursor)
    res1 = requests.get(url1).json()
    shortcodes = res1['graphql']['hashtag']['edge_hashtag_to_media']['edges']

    for shortcode in shortcodes:
        sc = shortcode['node']['shortcode']
        url2 = 'https://www.instagram.com/p/{}/?__a=1'.format(sc)
        res2 = requests.get(url2).json()
        username = res2['graphql']['shortcode_media']['owner']['username']

        count += 1
        print(count, sc, username)

        is_video = res2['graphql']['shortcode_media']['is_video']
        if is_video == True:
            filename = "{} {}.mp4".format(count, username)
            url_media = res2['graphql']['shortcode_media']['video_url']
        else:
            filename = "{} {}.jpg".format(count, username)
            url_media = res2['graphql']['shortcode_media']['display_url']

        path = 'media_download/{}/{}'.format(hashtag, filename)
        r_url_media = requests.get(url_media).content
        open(path, 'wb').write(r_url_media)
    end_cursor = res1['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
    has_next = res1['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
    if has_next == False: break
