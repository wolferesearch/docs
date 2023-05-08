import pandas as pd
import json
class NLPApi:
    
    def __init__(self, connection):
        self.connection = connection

    def compute_sentiment(self, list_of_texts: list, model='analyst-tone'):
        payload = {
            "texts" : list_of_texts
        }
        response = self.connection._post_(svc = 'sentiment/{}'.format(model), body = payload)
        return pd.DataFrame(json.loads(response.content.decode("utf-8"))['metrics'])
    
    


