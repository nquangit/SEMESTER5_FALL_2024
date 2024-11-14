import urllib.request
import json

url = input('Enter location: ')
if len(url) < 1 : 
    url = 'http://py4e-data.dr-chuck.net/comments_2091009.json'

print('Retrieving', url)
uh = urllib.request.urlopen(url)
raw_data = uh.read()
print('Retrieved',len(raw_data),'characters')

parsed_data = json.loads(raw_data)

data = []

for comment in parsed_data['comments']:
    data.append(comment['count'])

print('Count:', len(data))
print('Sum:', sum(data))