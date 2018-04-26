from apiclient import discovery

TMPL = '''
    User: %s
    Date: %s
    Post: %s
'''

API_KEY = 'AIzaSyA2poakKGR3cO6_KB6D28PsYygR7-_9H_g'
GPLUS = discovery.build('plus', 'v1', developerKey=API_KEY)
items = GPLUS.activities().search(query='python').execute().get('items', [])
for data in items:
    post = ' '.join(data['title'].strip().split())
    if post:
        print(TMPL % (data['actor']['displayName'],data['published'], post))
