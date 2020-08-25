# instagram comment yg diambil hanya comment pada postingan bukan comment atas comment
# sedangkan count di ig adalah semua comment baik pada postingan atau comment atas comment

import requests, json, time, csv

url = "https://www.instagram.com/graphql/query"
query_hash = 'bc3296d1ce80a24b1b6e40b1e72903f5'

end_cursor = ''
shortcode = input('Please enter shortcode: ')
# shortcode = "CET5U7ap-JJ"
count = 0
counter_file = 1
jml_per_file = 1000

# csv start here
writer = csv.writer(open('result_comment/{}_{}.csv'.format(shortcode, counter_file), 'w', newline=''))
header = ['Username', 'Comment']
writer.writerow(header)

while 1:
    variables = {
        "shortcode":shortcode,
        "first":50,
        'after': end_cursor
    }

    params = {
        'query_hash': query_hash,
        'variables': json.dumps(variables),

    }

    response = requests.get(url, params=params).json()

    try:
        comments = response['data']['shortcode_media']['edge_media_to_parent_comment']['edges']
    except:
        print("wait for 30 seconds..")
        time.sleep(30)
        continue
        # continue akan mengembalikan posisi eksekusi script ke variables

    for comment in comments:
        if count % jml_per_file == 0 and count != 0:
            counter_file += 1
            writer = csv.writer(open('result_comment/{}_{}.csv'.format(shortcode, counter_file), 'w', newline=''))
            writer.writerow(header)

        username = comment['node']['owner']['username']
        text = comment['node']['text']

        count += 1
        print(count, username, text)
        writer = csv.writer(open('result_comment/{}_{}.csv'.format(shortcode, counter_file), 'a', newline='', encoding='utf-8'))
        data = [username, text]
        writer.writerow(data)


    end_cursor  = response['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']
    # print(end_cursor)
    has_next = response['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
    if has_next == False: break
    time.sleep(2)