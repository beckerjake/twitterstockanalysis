import unirest
import json

response = unirest.post("https://smartcontent.dataninja.net/smartcontent/tag", headers = {"X-Mashape-Key":"o3xe9ExRlumshltWECAMuuM981vFp1tX6VDjsn4DPf6hvUuKia","Accept":"application/json","Content-Type":"application/json"},params=("{\"text\":\"Is there an overall sentiment score when there are no entities?.\", \"max_size\":10}"))

print(json.dumps(response.body, sort_keys = True, indent = 4, separators = (',', ': ')))
a = 1 + response.body['entity_list']["sentiment_score"]
print a
