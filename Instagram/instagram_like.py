import requests, json

url = "https://www.instagram.com/graphql/query"


shortcode = input('Please enter shortcode: ')
variables = {"shortcode":shortcode,"first":50}

params = {
    'query_hash': 'd5d763b1e2acf209d62d22d184488e57',
    'variables': json.dumps(variables)
}

response = requests.get(url, params=params).json()

users = response['data']['shortcode_media']['edge_liked_by']['edges']

count = 0
for user in users:

    username = user['node']['username']
    fullname = user['node']['full_name']
    profile = user['node']['profile_pic_url']
    count += 1
    print(username, fullname, profile)

print(count)
