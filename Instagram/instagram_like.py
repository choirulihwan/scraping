import requests, json, time, csv

url = "https://www.instagram.com/graphql/query"

end_cursor = ''
shortcode = input('Please enter shortcode: ')
count = 0
counter_file = 1
jml_per_file = 1000

# csv start here
writer = csv.writer(open('result_like/{}_{}.csv'.format(shortcode, counter_file), 'w', newline=''))
header = ['Username', 'Fullname', 'Profile']
writer.writerow(header)

while 1:
    variables = {
        "shortcode":shortcode,
        "first":50,
        'after': end_cursor
    }

    params = {
        'query_hash': 'd5d763b1e2acf209d62d22d184488e57',
        'variables': json.dumps(variables),

    }

    response = requests.get(url, params=params).json()

    try:
        users = response['data']['shortcode_media']['edge_liked_by']['edges']
    except:
        print("wait for 30 seconds..")
        time.sleep(30)
        continue
        # continue akan mengembalikan posisi eksekusi script ke variables

    for user in users:
        if count % jml_per_file == 0 and count != 0:
            counter_file += 1
            writer = csv.writer(open('result_like/{}_{}.csv'.format(shortcode, counter_file), 'w', newline=''))
            writer.writerow(header)

        username = user['node']['username']
        fullname = user['node']['full_name']
        profile = user['node']['profile_pic_url']
        count += 1
        print(count, username, fullname, profile)
        writer = csv.writer(open('result_like/{}_{}.csv'.format(shortcode, counter_file), 'a', newline='', encoding='utf-8'))
        data = [username, fullname, profile]
        writer.writerow(data)

    # "after":"QVFBanhPcUZtY0hhQTFIWko5OURuVkd5N0c5NDZuRlR3cjNEOHZvWVdxbS0zMHNXZTVSaVQxdEFIOFNzV2xSRDFXNUNiUHhWV1ZFNTBtZlBPRmg1ZkhYOA=="
    end_cursor  = response['data']['shortcode_media']['edge_liked_by']['page_info']['end_cursor']
    # print(end_cursor)
    has_next = response['data']['shortcode_media']['edge_liked_by']['page_info']['has_next_page']
    if has_next == False: break
    time.sleep(2)