from apiclient.discovery import build
from slugify import slugify
from random import randint

searchTerm = 'butter'

service = build("customsearch", "v1",developerKey="AIzaSyB4hl9a1RPB_MmuqPm_zNmO49Y20qSf9e4")
res = service.cse().list(
    q=slugify(searchTerm),
    cx='7204b6b1decb42058',
    searchType='image',
    imgSize="MEDIUM",
    safe='high'
    ).execute()

if not 'items' in res:
    print("🤖🦇 Could not find any matching image")
else:
    length = len(res['items'])
    print(res['items'][randint(0, length - 1)]['link'])
