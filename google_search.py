#Google developers custom search API

from googleapiclient.discovery import build
import pprint

api_key = "AIzaSyATvDtrZD_wt9pu4TOaSr9ITE1WGNC39pU"
cse_id = "010459714317855979319:-qrjznetymc"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

query_list = ['mondego','machine learning','software engineering','security','student affairs','Crista Lopes','graduate courses', 'REST','computer games','information retrieval']
query_list = [s + '  site:www.ics.uci.edu' for s in query_list]

for item in query_list:
	results = google_search(item, api_key, cse_id, num=5)
	print item+":"
	for result in results:
		pprint.pprint(result['link'])